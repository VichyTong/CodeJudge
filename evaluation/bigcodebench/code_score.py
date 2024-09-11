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
    test_case, model, analyze_prompt, compare_prompt, temperature, file_name, overwrite
):
    data = []
    with open(f"./data/bigcodebench/test_cases/{test_case}.jsonl") as f:
        for line in f:
            data.append(json.loads(line))

    if os.path.exists(f"./output/bigcodebench/{test_case}/" + file_name) and not overwrite:
        with open(f"./output/bigcodebench/{test_case}/" + file_name) as f:
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
    return data, out


def single_step_workflow(
    test_case,
    model,
    compare_prompt,
    temperature,
    file_name,
    return_type,
    overwrite,
):
    data, out = read_data(
        test_case, model, None, compare_prompt, temperature, file_name, overwrite
    )

    if overwrite:
        start_index = 0
    else:
        if len(out["data"]) == len(data):
            return
        start_index = len(out["data"])

    terminators, pipeline = load_model(model)
    for item in tqdm(data[start_index:]):
        program = item["program"]
        problem = item["problem"]
        canonical_solution = item["solution"]

        code_gpt_answer = form_filling(
            model,
            compare_prompt,
            terminators,
            pipeline,
            temperature,
            info={
                "CODE1": program,
                "CODE2": canonical_solution,
                "PROBLEM": problem,
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
            "question_id": item["task_id"],
        }
        out["data"].append(new_result)

        test_name = test_case.split(".")[0]
        directory_path = f"./output/bigcodebench/{test_name}/"
        os.makedirs(directory_path, exist_ok=True)

        with open(f"./output/bigcodebench/{test_name}/" + file_name, "w") as f:
            json.dump(out, f, indent=4)


def dual_step_workflow(
    test_case,
    model,
    analyze_prompt,
    compare_prompt,
    temperature,
    file_name,
    return_type,
    overwrite,
):
    data, out = read_data(
        test_case,
        model,
        analyze_prompt,
        compare_prompt,
        temperature,
        file_name,
        overwrite,
    )
    if overwrite:
        start_index = 0
    else:
        if len(out["data"]) == len(data):
            return
        start_index = len(out["data"])

    terminators, pipeline = load_model(model)

    for item in tqdm(data[start_index:]):
        program = item["program"]
        problem = item["problem"]
        canonical_solution = item["solution"]

        nl_mistakes = form_filling(
            model,
            compare_prompt,
            terminators,
            pipeline,
            temperature,
            info={
                "CODE1": program,
                "CODE2": canonical_solution,
                "PROBLEM": problem,
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
                "PROBLEM": problem,
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
            "question_id": item["task_id"],
        }
        out["data"].append(new_result)

        test_name = test_case.split(".")[0]
        directory_path = f"./output/bigcodebench/{test_name}/"
        os.makedirs(directory_path, exist_ok=True)
        with open(f"./output/bigcodebench/{test_name}/" + file_name, "w") as f:
            json.dump(out, f, indent=4)


def router(
    test_case,
    model,
    step,
    temperature,
    return_type,
    num_samples,
    overwrite,
    analyze_prompt=None,
    compare_prompt=None,
    file_name=None,
    num_index=None,
):
    if num_index is not None:
        full_file_name = f"{file_name}-sample-{num_index}.json"
        if step == 1:
            print(full_file_name)
            single_step_workflow(
                test_case,
                model,
                compare_prompt,
                temperature,
                full_file_name,
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
                return_type,
                overwrite,
            )
        return
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
    parser.add_argument("--return_type", type=str, default="bool")
    parser.add_argument("--num_index", type=int)
    parser.add_argument("--num_samples", type=int, default=1)
    parser.add_argument("--overwrite", action="store_true")

    args = parser.parse_args()

    test_case = args.test_case
    model = args.model
    step = args.step
    analyze_prompt_index = args.analyze_prompt
    compare_prompt_index = args.compare_prompt
    temperature = args.temperature
    return_type = args.return_type
    if args.num_index is not None:
        num_index = args.num_index
    else:
        num_index = None
    num_samples = args.num_samples
    overwrite = args.overwrite

    if step == 1:
        analyze_prompt = None
        compare_prompt = single_step_prompt[compare_prompt_index]
        file_name = f"{model}-1-{compare_prompt_index}-{temperature}"
    elif step == 2:
        analyze_prompt = dual_step_prompt["analyze_prompt"][analyze_prompt_index]
        compare_prompt = dual_step_prompt["compare_prompt"][compare_prompt_index]
        file_name = (
            f"{model}-2-{analyze_prompt_index}-{compare_prompt_index}-{temperature}"
        )

    router(
        test_case,
        model,
        step,
        temperature,
        return_type,
        num_samples,
        overwrite,
        analyze_prompt=analyze_prompt,
        compare_prompt=compare_prompt,
        file_name=file_name,
        num_index=num_index,
    )


if __name__ == "__main__":
    main()
