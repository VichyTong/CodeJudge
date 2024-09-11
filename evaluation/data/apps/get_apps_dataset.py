import json
import os
import random


# set random seed
random.seed(42)

with open("results/all_codes.json", "r") as f:
    codes_data = json.load(f)

with open("results/all_results.json", "r") as f:
    results_data = json.load(f)

with open("test.json", "r") as f:
    test_file = sorted(json.load(f))

# create a directory `test_cases`
if not os.path.exists("test_cases"):
    os.makedirs("test_cases")

selected_dataset = {}

for index, item in enumerate(test_file):
    data = {}
    directory = f"APPS/test/{item}"
    question_file = f"{directory}/question.txt"
    solution_file = f"{directory}/solutions.json"

    with open(question_file, "r") as f:
        question = f.read().strip()
        data["question"] = question
    with open(solution_file, "r") as f:
        solution = json.load(f)
        # randomly select one solution
        random_index = random.randint(0, len(solution) - 1)
        data["solution"] = solution[random_index]
    selected_dataset[str(index)] = data

generated_test_cases = {}
for index, item in enumerate(test_file):
    data = {}
    data["task_id"] = item
    data["program"] = codes_data[str(index)]
    data["problem"] = selected_dataset[str(index)]["question"]
    data["solution"] = selected_dataset[str(index)]["solution"]
    passed = True
    for result in results_data[str(index)][0]:
        if result != True:
            passed = False
            break
    data["pass"] = True if passed else False
    generated_test_cases[str(index)] = data

with open("test_cases/gpt.jsonl", "w") as f:
    for key in generated_test_cases:
        f.write(json.dumps(generated_test_cases[key]) + "\n")
