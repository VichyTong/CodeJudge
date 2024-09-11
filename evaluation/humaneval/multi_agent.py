import os
import json
import sys
import argparse

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from code_model_score import form_filling, answer_to_score
from multi_agent_prompts import template_prompt, final_prompt

from transformers import LlamaTokenizer
import transformers
import torch
from tqdm import tqdm


def read_data(test_cases, model, temperature, file_name):
    language = test_cases.split("-")[0]
    with open(f"./data/humaneval/dataset/{language}.json") as f:
        dataset = json.load(f)

    data = []
    with open(f"./data/humaneval/test_cases/{test_cases}.jsonl") as f:
        for line in f:
            data.append(json.loads(line))

    test_name = test_cases.split(".")[0]
    if os.path.exists(f"./output/humaneval/{test_name}/" + file_name):
        with open(f"./output/humaneval/{test_name}/" + file_name) as f:
            out = json.load(f)
    else:
        out = {
            "parameters": {
                "model": model,
                "temperature": temperature,
            },
            "data": [],
        }
    return data, dataset, out


def get_pair(item, dataset, with_prefix):
    question_id = item["question_id"]
    if with_prefix:
        canonical_solution = (
            dataset[question_id]["declaration"]
            + dataset[question_id]["canonical_solution"]
        )
        program = dataset[question_id]["declaration"] + item["program"]
    else:
        canonical_solution = dataset[question_id]["canonical_solution"]
        program = item["program"]
        # Some programs are empty
        if program == "":
            program = "<empty>"

    return program, canonical_solution


def one_by_one_workflow(
    test_case,
    model,
    temperature,
    file_name,
    with_prefix,
    return_type,
    tokenizer,
    pipeline,
):
    data, dataset, out = read_data(test_case, model, temperature, file_name)
    if len(out["data"]) == len(data):
        return

    with open("./data/humaneval/nl.json", "r") as f:
        nl = json.load(f)
    with open("./data/humaneval/example.json", "r") as f:
        example = json.load(f)

    for item in tqdm(data[len(out["data"]) :]):
        program, canonical_solution = get_pair(item, dataset, with_prefix)

        history = ""
        analysis_0 = form_filling(
            model,
            template_prompt,
            tokenizer,
            pipeline,
            temperature,
            info={
                "CODE1": program,
                "CODE2": canonical_solution,
                "PROBLEM": nl[item["question_id"]],
                "EXAMPLE": example[item["question_id"]],
                "HISTORY": history,
                "ROLE": "You are a professional programmer.",
                "NAME": "Alice",
            },
        )

        history = "Here is the discussion history:\n"
        history += "Alice: " + analysis_0 + "\n"

        analysis_1 = form_filling(
            model,
            template_prompt,
            tokenizer,
            pipeline,
            temperature,
            info={
                "CODE1": program,
                "CODE2": canonical_solution,
                "PROBLEM": nl[item["question_id"]],
                "EXAMPLE": example[item["question_id"]],
                "HISTORY": history,
                "ROLE": "You are a professional programmer.",
                "NAME": "Bob",
            },
        )

        history += "Bob: " + analysis_1 + "\n"

        analysis_2 = form_filling(
            model,
            template_prompt,
            tokenizer,
            pipeline,
            temperature,
            info={
                "CODE1": program,
                "CODE2": canonical_solution,
                "PROBLEM": nl[item["question_id"]],
                "EXAMPLE": example[item["question_id"]],
                "HISTORY": history,
                "ROLE": "You are a professional programmer.",
                "NAME": "Charlie",
            },
        )

        history += "Charlie: " + analysis_2 + "\n"

        final_answer = form_filling(
            model,
            final_prompt,
            tokenizer,
            pipeline,
            temperature,
            info={
                "HISTORY": history,
            },
        )

        code_gpt_score = answer_to_score(final_answer, return_type)
        new_result = {
            "pass": item["pass"],
            "program": program,
            "canonical_solution": canonical_solution,
            "code_gpt_score": {
                "code_gpt_score": float(code_gpt_score),
                "history": history,
                "final_answer": final_answer,
            },
            "question_id": item["question_id"],
        }
        out["data"].append(new_result)

        test_name = test_case.split(".")[0]
        directory_path = f"./output/humaneval/{test_name}/"
        os.makedirs(directory_path, exist_ok=True)
        with open(f"./output/humaneval/{test_name}/" + file_name, "w") as f:
            json.dump(out, f, indent=4)


def router(
    test_case,
    model,
    judge_type,
    temperature,
    with_prefix,
    return_type,
    num_samples,
):
    if model.startswith("CodeLlama"):
        model_path = f"./model/{model}-hf"
        tokenizer = LlamaTokenizer.from_pretrained(model_path)
        pipeline = transformers.pipeline(
            "text-generation",
            model=model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            return_full_text=False,
        )
    elif model.startswith("gpt"):
        tokenizer = None
        pipeline = None
    else:
        raise ("Invalid model name")

    for index in range(num_samples):
        if not with_prefix:
            file_name = f"{model}-multi-agent-{judge_type}-{temperature}-without-prefix-sample-{index}.json"
        else:
            file_name = (
                f"{model}-multi-agent-{judge_type}-{temperature}-sample-{index}.json"
            )
        print(file_name)
        if judge_type == "one_by_one":
            one_by_one_workflow(
                test_case,
                model,
                temperature,
                file_name,
                with_prefix,
                return_type,
                tokenizer,
                pipeline,
            )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--test_case", type=str)
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("--judge_type", type=str, default="one_by_one")
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--with_prefix", action="store_true")
    parser.add_argument("--return_type", type=str, default="bool")
    parser.add_argument("--num_samples", type=int, default=1)

    args = parser.parse_args()

    test_case = args.test_case
    model = args.model
    judge_type = args.judge_type
    temperature = args.temperature
    with_prefix = args.with_prefix
    return_type = args.return_type
    num_samples = args.num_samples

    router(
        test_case,
        model,
        judge_type,
        temperature,
        with_prefix,
        return_type,
        num_samples,
    )


if __name__ == "__main__":
    main()
