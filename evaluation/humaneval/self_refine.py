import json
import copy
import os
from code_score import router
from self_refine_prompt import analyze_prompt, failure_cases_prompt, refine_prompt
from prompts import single_step_prompt, dual_step_prompt
from code_model_score import form_filling
import argparse

language_list = [
    "cpp",
    "python",
    "java",
    "js",
]

model_temperature_map = {"gpt-3.5-turbo-1106": 0.0, "Meta-Llama-3-70B-Instruct": 0.4}

file_name_map = {
    "no_ref": "2-0-0-0.0",
    "with_ref": "2-0-1-0.0",
}

with open("./data/humaneval/nl.json", "r") as f:
    nl = json.load(f)


max_example_num = 3


def check_result(test_case, result_name):
    with open(f"./output/humaneval/{test_case}/{result_name}-sample-0.json", "r") as f:
        data = json.load(f)["data"]

    failed_cases = []
    acc_count = 0
    for item in data:
        if int(item["pass"]) == int(item["code_gpt_score"]["code_gpt_score"]):
            acc_count += 1
        else:
            failed_cases.append(item)

    acc = acc_count / len(data)
    return failed_cases, acc


def init(task_type, model):
    for language in language_list:
        test_case = f"{language}-small-validation"
        analyze_prompt = dual_step_prompt["analyze_prompt"][0]
        if task_type == "no_ref":
            compare_prompt = dual_step_prompt["compare_prompt"][0]
        elif task_type == "with_ref":
            compare_prompt = dual_step_prompt["compare_prompt"][1]
        router(
            test_case=test_case,
            model=model,
            step=2,
            temperature=model_temperature_map[model],
            with_prefix=True,
            return_type="bool",
            num_samples=1,
            overwrite=False,
            analyze_prompt=analyze_prompt,
            compare_prompt=compare_prompt,
            file_name=f"{model}-{file_name_map[task_type]}",
        )

    total_failed_cases = []
    acc_list = []
    for language in language_list:
        test_case = f"{language}-small-validation"
        file_name = f"{model}-{file_name_map[task_type]}"
        failed_cases, acc = check_result(test_case, file_name)
        total_failed_cases.extend(failed_cases)
        acc_list.append(acc)

    print(">>> Prompt Step 0:")
    print("'''")
    print(compare_prompt[0]["content"])
    print("'''")
    print(">>> acc:")
    print(acc_list)

    run(task_type, model, compare_prompt, total_failed_cases, 1)


def analyze(model, compare_prompt, failed_cases):
    failed_cases_text = ""
    cnt = 0
    for index, case in enumerate(failed_cases, start=1):
        if case["pass"]:
            ground_truth = "Yes"
        else:
            ground_truth = "No"
        model_output = case["code_gpt_score"]["parsed_comparison"]
        problem = nl[case["question_id"]]
        failed_cases_text += failure_cases_prompt.format(
            INDEX=index,
            PROBLEM=problem,
            CODE1=case["program"].strip(),
            GROUND_TRUTH=ground_truth,
            MODEL_OUTPUT=model_output,
        )
        cnt += 1
        if cnt == max_example_num:
            break

    input_analyze_prompt = copy.deepcopy(analyze_prompt)
    input_analyze_prompt[0]["content"] = input_analyze_prompt[0]["content"].format(
        PROMPT=compare_prompt, FAILURE_CASES=failed_cases_text
    )

    analysis = form_filling(
        model="gpt-4",
        prompt=input_analyze_prompt,
        terminators=None,
        pipeline=None,
        temperature=model_temperature_map[model],
    )
    print(">>> ANALYSIS")
    print(analysis)
    print("")

    input_refine_prompt = copy.deepcopy(refine_prompt)
    input_refine_prompt[0]["content"] = input_refine_prompt[0]["content"].format(
        PROMPT=compare_prompt[0]["content"], ANALYSIS=analysis
    )

    new_prompt = form_filling(
        model="gpt-4",
        prompt=input_refine_prompt,
        terminators=None,
        pipeline=None,
        temperature=model_temperature_map[model],
    )

    print(">>> NEW_PROMPT")
    print(new_prompt)
    print("")

    compare_prompt[0]["content"] = new_prompt
    return compare_prompt



def run(task_type, model, compare_prompt, total_failed_cases, step):
    if step == max_step + 1:
        return
    file_name = f"{model}-{file_name_map[task_type]}-step-{step}"
    already_run = False
    print(file_name)
    
    for language in language_list:
        test_case = f"{language}-small-validation"
        if os.path.exists(f"output/humaneval/{test_case}/{file_name}-sample-0.json"):
            with open(f"output/humaneval/{test_case}/{file_name}-sample-0.json", "r") as f:
                data = json.load(f)
                compare_prompt = data["parameters"]["compare_prompt"]
                already_run = True
                print(f">>> Step {step} has already been run for {language}; adapt the prompt accordingly.")
                break

    if not already_run:
        compare_prompt = analyze(model, compare_prompt, total_failed_cases)

    for language in language_list:
        test_case = f"{language}-small-validation"
        analyze_prompt = dual_step_prompt["analyze_prompt"][0]
        router(
            test_case=test_case,
            model=model,
            step=2,
            temperature=model_temperature_map[model],
            with_prefix=True,
            return_type="bool",
            num_samples=1,
            overwrite=False,
            analyze_prompt=analyze_prompt,
            compare_prompt=compare_prompt,
            file_name=file_name,
        )

    total_failed_cases = []
    acc_list = []
    for language in language_list:
        test_case = f"{language}-small-validation"
        failed_cases, acc = check_result(test_case, file_name)
        total_failed_cases.extend(failed_cases)
        acc_list.append(acc)

    print(f">>> Prompt Step {step}:")
    print("'''")
    print(compare_prompt[0]["content"])
    print("'''")
    print(">>> acc:")
    print(acc_list)

    run(task_type, model, compare_prompt, total_failed_cases, step + 1)

def best_prompt(task_type, model):
    acc_list = []
    if task_type == "no_ref":
        compare_prompt = dual_step_prompt["compare_prompt"][0]
    elif task_type == "with_ref":
        compare_prompt = dual_step_prompt["compare_prompt"][1]

    for language in language_list:
        test_case = f"{language}-small-validation"
        file_name = f"{model}-{file_name_map[task_type]}"
        _, acc = check_result(test_case, file_name)
        acc_list.append(acc)

    print(">>> Prompt Step 0:")
    # print("'''")
    # print(compare_prompt[0]["content"])
    # print("'''")
    print(">>> acc:")
    print(acc_list)

    for step in range(1, max_step + 1):
        acc_list = []
        file_name = f"{model}-{file_name_map[task_type]}-step-{step}"
        for language in language_list:
            test_case = f"{language}-small-validation"
            _, acc = check_result(test_case, file_name)
            acc_list.append(acc)
            with open(f"output/humaneval/{test_case}/{file_name}-sample-0.json", "r") as f:
                data = json.load(f)
                compare_prompt = data["parameters"]["compare_prompt"]
        
        print(f">>> Prompt Step {step}:")
        # print("'''")
        # print(compare_prompt[0]["content"])
        # print("'''")
        print(">>> acc:")
        print(acc_list)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_type", type=str, default="no_ref")
    parser.add_argument("--model", type=str, default="Meta-Llama-3-70B-Instruct")
    parser.add_argument("--max_step", type=int, default=3)
    
    args = parser.parse_args()
    global max_step
    max_step = args.max_step
    init(args.task_type, args.model)
    best_prompt(args.task_type, args.model)


if __name__ == "__main__":
    main()
