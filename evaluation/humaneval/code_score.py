import os
import json
import sys
import argparse

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from code_model_score import form_filling, answer_to_score, load_model
from prompts import single_step_prompt, dual_step_prompt

import torch
from tqdm import tqdm


def read_data(
    test_cases, model, analyze_prompt, compare_prompt, temperature, file_name, overwrite
):
    language = test_cases.split("-")[0]
    with open(f"./data/humaneval/dataset/{language}.json") as f:
        dataset = json.load(f)

    data = []
    with open(f"./data/humaneval/test_cases/{test_cases}.jsonl") as f:
        for line in f:
            data.append(json.loads(line))

    test_name = test_cases.split(".")[0]
    if os.path.exists(f"./output/humaneval/{test_name}/" + file_name) and not overwrite:
        with open(f"./output/humaneval/{test_name}/" + file_name) as f:
            out = json.load(f)
    else:
        if analyze_prompt is not None:
            out = {
                "parameters": {
                    "model": model,
                    "analyze_prompt": analyze_prompt,
                    "compare_prompt": compare_prompt,
                    "temperature": temperature,
                },
                "data": [],
            }
        else:
            out = {
                "parameters": {
                    "model": model,
                    "compare_prompt": compare_prompt,
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


def single_step_workflow(
    test_case,
    model,
    compare_prompt,
    temperature,
    file_name,
    with_prefix,
    return_type,
    overwrite,
):
    data, dataset, out = read_data(
        test_case, model, None, compare_prompt, temperature, file_name, overwrite
    )

    with open("./data/humaneval/nl.json", "r") as f:
        nl = json.load(f)
    with open("./data/humaneval/example.json", "r") as f:
        example = json.load(f)

    if overwrite:
        start_index = 0
    else:
        if len(out["data"]) == len(data):
            return
        start_index = len(out["data"])

    terminators, pipeline = load_model(model)
    for item in tqdm(data[start_index:]):
        program, canonical_solution = get_pair(item, dataset, with_prefix)

        code_gpt_answer = form_filling(
            model,
            compare_prompt,
            terminators,
            pipeline,
            temperature,
            info={
                "CODE1": program,
                "CODE2": canonical_solution,
                "PROBLEM": nl[item["question_id"]],
                "EXAMPLE": example[item["question_id"]],
                "LANGUAGE": test_case.split("-")[0],
            },
        )
        code_gpt_score = answer_to_score(code_gpt_answer, return_type)
        new_result = {
            "pass": item["pass"],
            "program": program,
            "canonical_solution": canonical_solution,
            "code_gpt_score": {
                "code_gpt_score": float(code_gpt_score),
                "comparison": code_gpt_answer,
            },
            "question_id": item["question_id"],
        }
        out["data"].append(new_result)

        test_name = test_case.split(".")[0]
        directory_path = f"./output/humaneval/{test_name}/"
        os.makedirs(directory_path, exist_ok=True)

        with open(f"./output/humaneval/{test_name}/" + file_name, "w") as f:
            json.dump(out, f, indent=4)


def dual_step_workflow(
    test_case,
    model,
    analyze_prompt,
    compare_prompt,
    temperature,
    file_name,
    with_prefix,
    return_type,
    overwrite,
):
    data, dataset, out = read_data(
        test_case,
        model,
        analyze_prompt,
        compare_prompt,
        temperature,
        file_name,
        overwrite,
    )

    with open("./data/humaneval/nl.json", "r") as f:
        nl = json.load(f)
    with open("./data/humaneval/example.json", "r") as f:
        example = json.load(f)

    if overwrite:
        start_index = 0
    else:
        if len(out["data"]) == len(data):
            return
        start_index = len(out["data"])

    terminators, pipeline = load_model(model)

    for item in tqdm(data[start_index:]):
        program, canonical_solution = get_pair(item, dataset, with_prefix)

        nl_mistakes = form_filling(
            model,
            compare_prompt,
            terminators,
            pipeline,
            temperature,
            info={
                "CODE1": program,
                "CODE2": canonical_solution,
                "PROBLEM": nl[item["question_id"]],
                "EXAMPLE": example[item["question_id"]],
                "LANGUAGE": test_case.split("-")[0],
            },
        )

        code_gpt_answer = form_filling(
            model,
            analyze_prompt,
            terminators,
            pipeline,
            temperature,
            info={
                "MISTAKES": nl_mistakes,
                "PROBLEM": nl[item["question_id"]],
                "EXAMPLE": example[item["question_id"]],
            },
            max_tokens=10,
        )

        code_gpt_score = answer_to_score(code_gpt_answer, return_type)
        new_result = {
            "pass": item["pass"],
            "program": program,
            "canonical_solution": canonical_solution,
            "code_gpt_score": {
                "code_gpt_score": float(code_gpt_score),
                "comparison": nl_mistakes,
                "parsed_comparison": code_gpt_answer,
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
    step,
    temperature,
    with_prefix,
    return_type,
    num_samples,
    overwrite,
    analyze_prompt=None,
    compare_prompt=None,
    file_name=None,
):
    for index in range(num_samples):
        full_file_name = f"{file_name}-sample-{index}.json"
        if step == 1:
            print(full_file_name)
            single_step_workflow(
                test_case,
                model,
                compare_prompt,
                temperature,
                full_file_name,
                with_prefix,
                return_type,
                overwrite,
            )
        elif step == 2:
            print(full_file_name)
            dual_step_workflow(
                test_case,
                model,
                analyze_prompt,
                compare_prompt,
                temperature,
                full_file_name,
                with_prefix,
                return_type,
                overwrite,
            )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--test_case", type=str)
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--analyze_prompt", type=int, default=0)
    parser.add_argument("--compare_prompt", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--with_prefix", action="store_true")
    parser.add_argument("--return_type", type=str, default="bool")
    parser.add_argument("--num_samples", type=int, default=1)
    parser.add_argument("--overwrite", action="store_true")

    args = parser.parse_args()

    test_case = args.test_case
    model = args.model
    step = args.step
    analyze_prompt_index = args.analyze_prompt
    compare_prompt_index = args.compare_prompt
    temperature = args.temperature
    with_prefix = args.with_prefix
    return_type = args.return_type
    num_samples = args.num_samples
    overwrite = args.overwrite

    if step == 1:
        analyze_prompt = None
        compare_prompt = single_step_prompt[compare_prompt_index]
        if not with_prefix:
            file_name = f"{model}-1-{compare_prompt_index}-{temperature}-without-prefix"
        else:
            file_name = (
                f"{model}-1-{compare_prompt_index}-{temperature}"
            )
    elif step == 2:
        analyze_prompt = dual_step_prompt["analyze_prompt"][analyze_prompt_index]
        compare_prompt = dual_step_prompt["compare_prompt"][compare_prompt_index]
        if not with_prefix:
            file_name = f"{model}-2-{analyze_prompt_index}-{compare_prompt_index}-{temperature}-without-prefix"
        else:
            file_name = f"{model}-2-{analyze_prompt_index}-{compare_prompt_index}-{temperature}"

    router(
        test_case,
        model,
        step,
        temperature,
        with_prefix,
        return_type,
        num_samples,
        overwrite,
        analyze_prompt=analyze_prompt,
        compare_prompt=compare_prompt,
        file_name=file_name,
    )


if __name__ == "__main__":
    main()
