import os
import json

from scipy import stats
from numpy import nanmean

NUM_RUNS = 3

conala_test_cases = [
    "baseline",
    "tranx-annot",
    "best-tranx",
    "best-tranx-rerank",
    "codex",
]


def extend(array):
    """
    Extend a list of lists to a list
    Examples:
        [[1, 2], [3, 4]] -> [1, 2, 3, 4]
    """
    return [item for sublist in array for item in sublist]


def print_number(kendalltau, pearsonr, spearmanr, length=None):
    print("{:.3f}".format(round(kendalltau, 3)), end=" | ")
    print("{:.3f}".format(round(pearsonr, 3)), end=" | ")
    print("{:.3f}".format(round(spearmanr, 3)), end=" | ")
    if length:
        print(length, end=" | ")
    print("")


def print_correlation(file_name):
    print(file_name.split("/")[-1], end=" | ")
    references, predictions = [], []
    with open(file_name, "r") as f:
        data = json.load(f)

    for d in data["data"]:
        references.append([float(d["grade"][k]) for k in conala_test_cases])
        predictions.append(
            [float(d["code_gpt_score"][k]["code_gpt_score"]) for k in conala_test_cases]
        )

    kendalltau = nanmean(
        [
            stats.kendalltau(reference, prediction).statistic
            for reference, prediction in zip(references, predictions)
        ]
    )
    pearsonr = nanmean(
        [
            stats.pearsonr(reference, prediction).statistic
            for reference, prediction in zip(references, predictions)
        ]
    )
    spearmanr = nanmean(
        [
            stats.spearmanr(reference, prediction).statistic
            for reference, prediction in zip(references, predictions)
        ]
    )
    length = len(references)
    print_number(kendalltau, pearsonr, spearmanr, length)


def print_other_correlation(file_name):
    print("")
    print(file_name.split("/")[-1])
    references = []
    predictions = {
        "bleu": [],
        "codebleu": [],
        "chrf": [],
        "rougeL": [],
        "ruby": [],
        "meteor": [],
        "CodeBERTScore_f1": [],
        "CodeBERTScore_f3": [],
    }

    with open(file_name, "r") as f:
        data = json.load(f)

    def add_data(x):
        references.append([float(x["grade"][k]) for k in conala_test_cases])

        for key in predictions:
            predictions[key].append(
                [float(x["metrics_score"][k][key]) for k in conala_test_cases]
            )

    for item in data:
        add_data(item)

    for key in predictions:
        print(key, end=" | ")
        kendalltau = stats.kendalltau(
            extend(references), extend(predictions[key])
        ).statistic
        pearsonr = stats.pearsonr(
            extend(references), extend(predictions[key])
        ).statistic
        spearmanr = stats.spearmanr(
            extend(references), extend(predictions[key])
        ).statistic
        print_number(kendalltau, pearsonr, spearmanr)


def main():
    file_list = []
    for file_name in os.listdir(f"output/conala"):
        if file_name.startswith("gpt") or file_name.startswith("CodeLlama"):
            file_list.append(file_name)

    file_list.sort(key=lambda x: x)

    for file_name in file_list:
        print_correlation(f"output/conala/{file_name}")

    for index in range(NUM_RUNS):
        print_other_correlation(f"output/conala/other-metrics-sample-{index}.json")


if __name__ == "__main__":
    main()
