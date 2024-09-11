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

conala_test_cases = [
    "baseline",
    "tranx-annot",
    "best-tranx",
    "best-tranx-rerank",
    "codex",
]


def calculate_other_metric(output_file_name):
    language = "python"
    with open(f"./data/conala/conala.json") as f:
        dataset = json.load(f)

    out = []
    for item in tqdm(dataset):
        canonical_solution = item["snippet"]
        item["metrics_score"] = {}
        for case in conala_test_cases:
            program = item[case]
            _, _, f1, f3 = code_bert_score.score(
                cands=[program], refs=[canonical_solution], lang=language
            )
            f1 = f1.tolist()
            f3 = f3.tolist()
            item["metrics_score"][case] = {
                "bleu": bleu(canonical_solution, program),
                "codebleu": codebleu(canonical_solution, program),
                "chrf": chrf(canonical_solution, program),
                "rougel": rougel(canonical_solution, program),
                "ruby": ruby(canonical_solution, program),
                "meteor": meteor(canonical_solution, program),
                "code_bert_score_f1": f1[0],
                "code_bert_score_f3": f3[0],
            }

        out.append(item)

    with open(output_file_name, "w") as f:
        json.dump(out, f, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_samples", type=int, default=3)
    args = parser.parse_args()
    num_samples = args.num_samples

    for i in range(num_samples):
        if os.path.exists(f"./output/conala/other-metrics-sample-{i}.json"):
            continue
        calculate_other_metric(f"./output/conala/other-metrics-sample-{i}.json")


if __name__ == "__main__":
    main()
