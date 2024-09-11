import json
import os
import sys
import argparse
from tqdm.auto import tqdm
import code_bert_score

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from codegen_metrics import (
    codebleu,
    ruby,
    chrf,
    bleu,
    meteor,
    rougel,
)

def calculate_other_metric(test_case, with_prefix, i):
    language = test_case.split("-")[0]
    with open(f"./data/humaneval/dataset/{language}.json") as f:
        dataset = json.load(f)

    data = []
    with open(f"./data/humaneval/test_cases/{test_case}.jsonl") as f:
        for line in f:
            data.append(json.loads(line))

    out = []
    for item in tqdm(data):
        question_id = item["question_id"]
        if with_prefix:
            program = dataset[question_id]["declaration"] + item["program"]
            canonical_solution = (
                dataset[question_id]["declaration"]
                + dataset[question_id]["canonical_solution"]
            )

            output_name = f"other-metrics-sample-{i}.json"
        else:
            canonical_solution = dataset[question_id]["canonical_solution"]
            program = item["program"]
            output_name = f"other-metrics-without-prefix-sample-{i}.json"

        _, _, f1, f3 = code_bert_score.score(
            cands=[program], refs=[canonical_solution], lang=language
        )
        f1 = f1.tolist()
        f3 = f3.tolist()
        out.append(
            {
                "pass": item["pass"],
                "program": program,
                "canonical_solution": canonical_solution,
                "bleu": bleu(canonical_solution, program),
                "codebleu": codebleu(canonical_solution, program),
                "chrf": chrf(canonical_solution, program),
                "rougel": rougel(canonical_solution, program),
                "ruby": ruby(canonical_solution, program),
                "meteor": meteor(canonical_solution, program),
                "code_bert_score_f1": f1[0],
                "code_bert_score_f3": f3[0],
            }
        )

        with open(f"./output/humaneval/{test_case}/{output_name}", "w") as f:
            json.dump(out, f, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_case", type=str)
    parser.add_argument("--with_prefix", action="store_true")
    parser.add_argument("--num_samples", type=int, default=3)
    args = parser.parse_args()

    test_case = args.test_case
    with_prefix = args.with_prefix
    num_samples = args.num_samples
    if test_case is None:
        for i in range(num_samples):
            for language in ["python", "cpp", "java", "js"]:
                calculate_other_metric(f"{language}-small-test", with_prefix, i)
    else:
        for i in range(num_samples):
            calculate_other_metric(test_case, with_prefix, i)


if __name__ == "__main__":
    main()
