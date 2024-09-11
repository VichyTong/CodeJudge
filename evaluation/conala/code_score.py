import os
import json
import sys
import random
import argparse

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from code_model_score import form_filling, answer_to_score, load_model
from prompts import single_step_prompt, dual_step_prompt

import torch
from tqdm import tqdm


conala_test_cases = [
    "baseline",
    "tranx-annot",
    "best-tranx",
    "best-tranx-rerank",
    "codex",
]


def read_data(model, temperature, file_name, compare_prompt=None, analyze_prompt=None):
    with open("./data/conala/conala.json") as f:
        data = json.load(f)

    if os.path.exists(f"./output/conala/{file_name}"):
        with open(f"./output/conala/{file_name}") as f:
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
    model,
    compare_prompt,
    temperature,
    file_name,
    return_type,
):
    data, out = read_data(model, temperature, file_name, compare_prompt=compare_prompt)
    if len(out["data"]) == len(data):
        return

    terminators, pipeline = load_model(model)
    for item in tqdm(data[len(out["data"]) :]):
        reference = item["snippet"]
        problem = item["intent"]

        output_item = {
            "intent": item["intent"],
            "snippet": item["snippet"],
            "baseline": item["baseline"],
            "tranx-annot": item["tranx-annot"],
            "best-tranx": item["best-tranx"],
            "best-tranx-rerank": item["best-tranx-rerank"],
            "codex": item["codex"],
            "grade": item["grade"],
            "code_gpt_score": {},
        }

        for case in conala_test_cases:
            prediction = item[case]

            code_gpt_answer = form_filling(
                model,
                compare_prompt,
                terminators,
                pipeline,
                temperature,
                info={
                    "CODE1": prediction,
                    "CODE2": reference,
                    "PROBLEM": problem,
                }
            )

            output_item["code_gpt_score"][case] = {
                "code_gpt_score": float(answer_to_score(code_gpt_answer, return_type)),
                "comparison": code_gpt_answer,
            }

        out["data"].append(output_item)

        os.makedirs(f"./output/conala/", exist_ok=True)

        with open(f"./output/conala/" + file_name, "w") as f:
            json.dump(out, f, indent=4)


def dual_step_workflow(
    model,
    analyze_prompt,
    compare_prompt,
    temperature,
    file_name,
    return_type,
):
    data, out = read_data(
        model,
        temperature,
        file_name,
        analyze_prompt=analyze_prompt,
        compare_prompt=compare_prompt,
    )
    if len(out["data"]) == len(data):
        return

    terminators, pipeline = load_model(model)
    for item in tqdm(data[len(out["data"]) :]):
        reference = item["snippet"]
        problem = item["intent"]

        output_item = {
            "intent": item["intent"],
            "snippet": item["snippet"],
            "baseline": item["baseline"],
            "tranx-annot": item["tranx-annot"],
            "best-tranx": item["best-tranx"],
            "best-tranx-rerank": item["best-tranx-rerank"],
            "codex": item["codex"],
            "grade": item["grade"],
            "code_gpt_score": {},
        }

        for case in conala_test_cases:
            prediction = item[case]

            nl_mistakes = form_filling(
                model,
                compare_prompt,
                terminators,
                pipeline,
                temperature,
                info={
                    "CODE1": prediction,
                    "CODE2": reference,
                    "PROBLEM": problem,
                }
            )
            code_gpt_answer = form_filling(
                model,
                analyze_prompt,
                terminators,
                pipeline,
                temperature,
                info={
                    "MISTAKES": nl_mistakes,
                },
                max_tokens=10,
            )
            code_gpt_score = answer_to_score(code_gpt_answer, return_type)

            output_item["code_gpt_score"][case] = {
                "code_gpt_score": float(code_gpt_score),
                "comparison": nl_mistakes,
                "parsed_comparison": code_gpt_answer,
            }

        out["data"].append(output_item)
        os.makedirs(f"./output/conala/", exist_ok=True)
        with open(f"./output/conala/" + file_name, "w") as f:
            json.dump(out, f, indent=4)


def router(
    model,
    step,
    analyze_prompt_index,
    compare_prompt_index,
    temperature,
    return_type,
    num_samples,
    start_index,
):
    for index in range(start_index, start_index + num_samples):
        if step == 1:
            compare_prompt = single_step_prompt[compare_prompt_index]
            file_name = (
                f"{model}-1-{compare_prompt_index}-{temperature}-sample-{index}.json"
            )
            print(file_name)
            single_step_workflow(
                model,
                compare_prompt,
                temperature,
                file_name,
                return_type,
            )
        elif step == 2:
            analyze_prompt = dual_step_prompt["analyze_prompt"][analyze_prompt_index]
            compare_prompt = dual_step_prompt["compare_prompt"][compare_prompt_index]

            file_name = f"{model}-2-{analyze_prompt_index}-{compare_prompt_index}-{temperature}-sample-{index}.json"
            print(file_name)
            dual_step_workflow(
                model,
                analyze_prompt,
                compare_prompt,
                temperature,
                file_name,
                return_type,
            )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--analyze_prompt", type=int, default=0)
    parser.add_argument("--compare_prompt", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--return_type", type=str, default="bool")
    parser.add_argument("--num_samples", type=int, default=1)
    parser.add_argument("--start_index", type=int, default=0)

    args = parser.parse_args()

    model = args.model
    step = args.step
    analyze_prompt_index = args.analyze_prompt
    compare_prompt_index = args.compare_prompt
    temperature = args.temperature
    return_type = args.return_type
    num_samples = args.num_samples
    start_index = args.start_index

    router(
        model,
        step,
        analyze_prompt_index,
        compare_prompt_index,
        temperature,
        return_type,
        num_samples,
        start_index,
    )


if __name__ == "__main__":
    main()
