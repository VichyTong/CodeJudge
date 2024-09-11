import random
import json
import random

random.seed(42)

test_index = []
validation_index = []


def split_dataset(total_length):
    global test_index, validation_index

    total_index = list(range(total_length))
    random.shuffle(total_index)

    validation_index = total_index[: int(total_length * 0.2)]
    test_index = total_index[int(total_length * 0.2) :]


def create_dataset(language):
    file_path = f"data/{language}_test_results.jsonl"

    data = []
    with open(file_path) as f:
        for line in f:
            data.append(json.loads(line))

    out = {"test": [], "validation": []}

    data.sort(key=lambda x: int(x["task_id"].split("/")[1]))

    for index in test_index:
        item = data[index]
        out["test"].append(
            {
                "question_id": item["task_id"].split("/")[1],
                "program": item["generation"],
                "pass": item["passed"],
            }
        )

    for index in validation_index:
        item = data[index]
        out["validation"].append(
            {
                "question_id": item["task_id"].split("/")[1],
                "program": item["generation"],
                "pass": item["passed"],
            }
        )

    with open(f"../data/humaneval/test_cases/{language}-small-test.jsonl", "w") as f:
        for item in out["test"]:
            f.write(json.dumps(item) + "\n")

    with open(
        f"../data/humaneval/test_cases/{language}-small-validation.jsonl", "w"
    ) as f:
        for item in out["validation"]:
            f.write(json.dumps(item) + "\n")


def main():
    split_dataset(164)
    for language in ["cpp", "java", "python", "js", "go"]:
        create_dataset(language)


if __name__ == "__main__":
    main()
