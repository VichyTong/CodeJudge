import json
import os
import random
import argparse


def preprocess_file(model_name, platform):
    with open(
        f"sanitized_calibrated_samples/instruct/{model_name}--bigcodebench-instruct--{platform}-0-1-sanitized-calibrated_eval_results.json",
        "r",
    ) as f:
        data = json.load(f)["eval"]

    with open("dataset.jsonl", "r") as f:
        dataset = [json.loads(line) for line in f]

    output = []
    for name in data:
        detail = data[name][0]
        task_id = int(name.split("/")[-1])
        program = detail["solution"]
        is_pass = detail["status"] == "pass"

        prefix = dataset[task_id]["instruct_prompt"].strip().split("```")[-2].strip()

        output.append(
            {
                "task_id": task_id,
                "program": program,
                "problem": dataset[task_id]["instruct_prompt"],
                "solution": prefix + "\n" + dataset[task_id]["canonical_solution"],
                "pass": is_pass,
            }
        )

    # sort output
    output = sorted(output, key=lambda x: x["task_id"])

    # sample 10% of the data
    random.seed(42)
    random.shuffle(output)
    output = output[: int(len(output) * 0.1)]
    output = sorted(output, key=lambda x: x["task_id"])

    for item in output:
        item["task_id"] = str(item["task_id"])

    os.makedirs("test_cases", exist_ok=True)
    with open(f"test_cases/{model_name}.jsonl", "w") as f:
        for item in output:
            f.write(json.dumps(item) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess BigCodeBench data")
    parser.add_argument("--model_name", type=str, help="model name")
    parser.add_argument("--platform", type=str, help="platform")
    args = parser.parse_args()
    preprocess_file(args.model_name, args.platform)
