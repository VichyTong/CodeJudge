import json
import argparse
from scipy import stats


def extend(array):
    """
    Extend a list of lists to a list
    Examples:
        [[1, 2], [3, 4]] -> [1, 2, 3, 4]
    """
    return [item for sublist in array for item in sublist]


def calculate_correlation(file_name):
    references, predictions = [], []
    with open(file_name, "r") as f:
        data = json.load(f)

    invalid_cnt = 0
    for d in data["data"]:
        if d["code_gpt_score"]["code_gpt_score"] == -1.0:
            invalid_cnt += 1
            continue
        references.append([float(d["pass"])])
        predictions.append([float(d["code_gpt_score"]["code_gpt_score"])])

    kendalltau, _ = stats.kendalltau(extend(references), extend(predictions))
    spearmanr, _ = stats.spearmanr(extend(references), extend(predictions))

    kendalltau = round(kendalltau, 3)
    spearmanr = round(spearmanr, 3)
    return kendalltau, spearmanr, invalid_cnt, len(data["data"])


def print_correlation(file_name):
    print(file_name.split("/")[-1])
    kendalltau, spearmanr, invalid_cnt, total_cnt = calculate_correlation(file_name)
    print("kendalltau: {:.3f}".format(kendalltau))
    print("spearmanr: {:.3f}".format(spearmanr))
    print("invalid_cnt: {}/{}".format(invalid_cnt, total_cnt))


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
        references.append([float(x["pass"])])
        predictions["bleu"].append([float(x["bleu"])])
        predictions["codebleu"].append([float(x["codebleu"])])
        predictions["chrf"].append([float(x["chrf"])])
        predictions["rougeL"].append([float(x["rougel"])])
        predictions["ruby"].append([float(x["ruby"])])
        predictions["meteor"].append([float(x["meteor"])])
        predictions["CodeBERTScore_f1"].append([x["code_bert_score_f1"]])
        predictions["CodeBERTScore_f3"].append([x["code_bert_score_f3"]])

    for item in data:
        add_data(item)

    for key in predictions:
        print(key)
        kendalltau, k_p_value = stats.kendalltau(
            extend(references), extend(predictions[key])
        )
        spearmanr, s_p_value = stats.spearmanr(
            extend(references), extend(predictions[key])
        )
        print("kendalltau: {:.3f} ({:.3f})".format(kendalltau, k_p_value))
        print("spearmanr: {:.3f} ({:.3f})".format(spearmanr, s_p_value))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_case", type=str)
    parser.add_argument("--file_name", type=str)
    args = parser.parse_args()
    test_case = args.test_case
    file_name = args.file_name

    if file_name == "other-metrics.json":
        print_other_correlation(f"output/humaneval/{test_case}/{file_name}")
    else:
        print_correlation(f"output/humaneval/{test_case}/{file_name}")


if __name__ == "__main__":
    main()
