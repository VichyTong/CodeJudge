import datasets
import argparse
import gzip
import json
from pathlib import Path
from tqdm import tqdm
import sys
import os
from typing import List

TOP_P = 0.95
MAX_TOKENS = 512


def partial_arg_parser():
    args = argparse.ArgumentParser()

    args.add_argument(
        "--output-dir",
        type=str,
        help="Directory in which to place JSON files with completions. The default is root_dataset-lang-model_name-temperature-reworded",
    )

    args.add_argument(
        "--output-dir-prefix", type=str, help="Prefix for the output directory"
    )

    args.add_argument(
        "--use-local",
        action="store_true",
        help="Use this flag when running from local prompts.",
    )

    # Reuired when use local is passed
    args.add_argument(
        "--dataset",
        type=str,
        required="--use-local" in sys.argv,
        help="The local dataset in JSON format to get from this computer.",
    )
    # Only required when use local is not passed
    args.add_argument(
        "--lang",
        type=str,
        required="--use-local" not in sys.argv,
        help="Target language for completions",
    )
    args.add_argument(
        "--root-dataset",
        type=str,
        required="--use-local" not in sys.argv,
        help="either mbpp or humaneval",
    )
    args.add_argument("--temperature", type=float, required=True)
    args.add_argument(
        "--input-start-index",
        type=int,
        help="Index into the dataset. If omitted, starts from the beginning",
    )
    args.add_argument(
        "--input-limit", type=int, help="Number of items to process from the dataset"
    )
    args.add_argument("--completion-limit", type=int, default=200)
    args.add_argument(
        "--batch-size", type=int, default=16, help="Number of completions to batch"
    )
    args.add_argument(
        "--prompt-prefix", type=str, help="A prefix to prepend to every prompt"
    )
    return args

def make_main(args, model_name, gen_completions):

    assert "-" not in model_name, "Model name must not have hyphens"

    if args.output_dir is None:
        args.output_dir = (
            (
                f"{args.root_dataset}-{args.lang}-{model_name}-{args.temperature}-reworded"
            )
            if not args.use_local
            else (
                f"{args.dataset.split('/')[-1].split('.')[0]}-{model_name}-{args.temperature}-reworded"
            )
        )

    if args.output_dir_prefix is not None:
        args.output_dir = f"{args.output_dir_prefix}/{args.output_dir}"

    exp_dir = Path(args.output_dir)
    if not exp_dir.exists():
        exp_dir.mkdir()

    if args.use_local:
        problems = datasets.load_dataset("json", data_files=args.dataset, split="train")
    else:
        problems = datasets.load_dataset(
            "THUDM/humaneval-x", f"{args.lang}", split="test"
        )

    
    start_index = args.input_start_index if args.input_start_index is not None else 0
    stop_index = min(
        len(problems),
        start_index + args.input_limit
        if args.input_limit is not None
        else len(problems),
    )
    start_index = args.input_start_index if args.input_start_index is not None else 0
    stop_index = min(
        len(problems),
        start_index + args.input_limit
        if args.input_limit is not None
        else len(problems),
    )
    problems = problems.select(range(start_index, stop_index))

    # Read all existing completions
    all_completions = dict(read_completions(exp_dir, args.temperature, problem) for problem in problems)

    # Generate a list of prompts, including multiple copies when needed.
    problem_list = [ ]
    stop: List[str] = None
    for completions in all_completions.values():

        if stop is None:
            stop = completions["stop_tokens"]
        else:
            assert stop == completions["stop_tokens"], "Stop tokens must be the same for all completions"
        
        assert completions["temperature"] == args.temperature, "Temperature must be the same for all completions"

        if len(completions["generation"]) >= args.completion_limit:
            continue

        num_new_completions = args.completion_limit - len(completions["generation"])

        if args.prompt_prefix is not None:
            prompt = args.prompt_prefix +  completions["prompt"]
        else:
            prompt = completions["prompt"]
        item = { "prompt": prompt, "task_id": completions["task_id"] }

        problem_list.extend([ item for _ in range(num_new_completions) ])
    
    # Break problem_list into batches of size args.batch_size.
    problem_list = [ problem_list[i:i+args.batch_size] for i in range(0, len(problem_list), args.batch_size) ]

    
    for batch in tqdm(problem_list, unit="batch"):
        new_completions = gen_completions(
                prompts=[item["prompt"] for item in batch],
                max_tokens=MAX_TOKENS,
                temperature=args.temperature,
                top_p=TOP_P,
                stop=stop
        )
        modified_problems = set()
        for item, a_completion in zip(batch, new_completions):
            all_completions[item["task_id"]]["generation"].append(a_completion)
            modified_problems.add(item["task_id"])
        
        for name in modified_problems:
            os.makedirs(exp_dir, exist_ok=True)
            file_name = name.split("/")[1]
            with gzip.open(exp_dir / f"{file_name}.json.gz", "wt") as f:
                f.write(json.dumps(all_completions[name]))


def read_completions(exp_dir, temperature, problem):
    problem_filename = exp_dir / f"{problem['task_id']}.json.gz"
    if problem_filename.exists():
        with gzip.open(problem_filename, "rt") as f:
            existing = json.loads(f.read())
            return (existing["task_id"], existing)
    
    language = problem["task_id"].split('/')[0]
    if language.lower() == "cpp":
        stop_tokens = ["\n}"]
    elif language.lower() == "java":
        stop_tokens = ["\n    }\n"]
    elif language.lower() == "python":
        stop_tokens = ["\ndef", "\n#", "\nif", "\nclass"]
    elif language.lower() == "javascript":
        stop_tokens = ["\nfunction ", "\n/*", "\n//", "\nconsole.log"]
    elif language.lower() == "go":
        stop_tokens = ["\nfunc ", "\n//", "\n/*", "\npackage", "\nimport"]
    else:
        raise ValueError(f"Unknown language {language}")

    new_completions = {
        "task_id": problem["task_id"],
        "language": language,
        "temperature": temperature,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "prompt": problem["prompt"],
        "tests": problem["test"],
        "generation": [],
        "stop_tokens": stop_tokens,
    }
    return (new_completions["task_id"], new_completions)


def stop_at_stop_token(decoded_string, stop_tokens):
    """
    Produces the prefix of decoded_string that ends at the first occurrence of
    a stop_token.

    WARNING: the decoded_string *must not* include the prompt, which may have stop tokens
    itself.
    """
    min_stop_index = len(decoded_string)
    for stop_token in stop_tokens:
        stop_index = decoded_string.find(stop_token)
        if stop_index != -1 and stop_index < min_stop_index:
            min_stop_index = stop_index
    return decoded_string[:min_stop_index]