import json
from datasets import load_dataset

language_list = ["python", "cpp", "java", "js", "go"]

with open("nl.json", "r") as f:
    questions = json.load(f)

for language in language_list:
    data = load_dataset("THUDM/humaneval-x", language)

    output = {}
    for index, item in enumerate(data["test"]):
        output[index] = {
            "prompt": item["prompt"],
            "question": questions[item["task_id"].split('/')[1]],
            "declaration": item["declaration"],
            "canonical_solution": item["canonical_solution"],
        }
    
    with open(f"dataset/{language}.json", "w") as f:
        json.dump(output, f, indent=4)
