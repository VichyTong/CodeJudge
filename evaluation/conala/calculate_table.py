import json
import os

import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns
from sklearn.metrics import root_mean_squared_error

RUN_NUM = 1

conala_test_cases = [
    "baseline",
    "tranx-annot",
    "best-tranx",
    "best-tranx-rerank",
    "codex",
]

existed_metric_map = {
    "bleu": "BLEU",
    "rougeL": "ROUGE-L",
    "meteor": "METEOR",
    "chrf": "chrF",
    "codebleu": "CodeBLEU",
    "ruby": "RUBY",
    "CodeBERTScore_f1": "CodeBERTScore$_{f1}$",
    "CodeBERTScore_f3": "CodeBERTScore$_{f3}$",
}

model_temperature_map = {
    "CodeLlama-34b-Instruct": "0.4",
    "Meta-Llama-3-8B-Instruct": "0.4",
    "Meta-Llama-3-70B-Instruct": "0.4",
    "gpt-3.5-turbo-1106": "0.0",
}

model_name_map = {
    "CodeLlama-34b-Instruct": "Code Llama - Instruct 34B",
    "Meta-Llama-3-8B-Instruct": "Meta-Llama-3-8B-Instruct",
    "Meta-Llama-3-70B-Instruct": "Meta-Llama-3-70B-Instruct",
    "gpt-3.5-turbo-1106": "GPT-3.5-Turbo-1106",
}

method_map = {
    "1-1": "\\bool{}",
    "1-0": "\\bool{} w/o \\reference{}",
    "1-3": "ICE-Score",
    "1-2": "ICE-Score w/o \\reference{}",
    "2-0-1": "\\citeeval{}",
    "2-0-0": "\\citeeval{} w/o \\reference{}",
    # "1-5": "\\citeeval{}",
    # "1-4": "\\citeeval{} w/o \\reference{}",
}


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
    total_cnt = 0
    max_pred = 0
    for d in data["data"]:
        example_references = []
        example_predictions = []
        for k in conala_test_cases:
            total_cnt += 1
            example_references.append(float(d["grade"][k]))
            if d["code_gpt_score"][k]["code_gpt_score"] == -1:
                invalid_cnt += 1
                example_predictions.append(0)
            else:
                example_predictions.append(
                    float(d["code_gpt_score"][k]["code_gpt_score"])
                )
                max_pred = max(
                    max_pred, float(d["code_gpt_score"][k]["code_gpt_score"])
                )
        references.append(example_references)
        predictions.append(example_predictions)

    kendalltau = []
    spearmanr = []
    pearsonr = []
    for reference, prediction in zip(references, predictions):
        kendalltau.append(stats.kendalltau(reference, prediction).statistic)
        spearmanr.append(stats.spearmanr(reference, prediction).statistic)
        pearsonr.append(stats.pearsonr(reference, prediction).statistic)

    ref = extend(references)
    pred = extend(predictions)
    ref = [x / 4 for x in ref]
    if max_pred > 1:
        pred = [x / 4 for x in pred]
    rmse = root_mean_squared_error(ref, pred)

    return {
        "kendalltau": kendalltau,
        "spearmanr": spearmanr,
        "pearsonr": pearsonr,
        "invalid_cnt": invalid_cnt,
        "total_cnt": total_cnt,
        "rmse": rmse,
    }


def calculate_other_correlation(file_name):
    references = []
    predictions = {}
    for metric in existed_metric_map:
        predictions[metric] = []

    with open(file_name, "r") as f:
        data = json.load(f)

    for item in data:
        references.append([float(item["grade"][k]) for k in conala_test_cases])
        for key in predictions:
            predictions[key].append(
                [float(item["metrics_score"][k][key]) for k in conala_test_cases]
            )

    ref = extend(references)
    ref = [x / 4 for x in ref]
    pred = {}
    for key in predictions:
        pred[key] = extend(predictions[key])

    output = {}
    for key in predictions:
        kendalltau = [
            stats.kendalltau(reference, prediction).statistic
            for reference, prediction in zip(references, predictions[key])
        ]
        spearmanr = [
            stats.spearmanr(reference, prediction).statistic
            for reference, prediction in zip(references, predictions[key])
        ]
        pearsonr = [
            stats.pearsonr(reference, prediction).statistic
            for reference, prediction in zip(references, predictions[key])
        ]
        rmse = root_mean_squared_error(ref, pred[key])
        output[key] = (kendalltau, spearmanr, pearsonr, rmse)

    return output


def calculate():
    result = {}
    for index in range(RUN_NUM):
        other_metrics = calculate_other_correlation(
            f"output/conala/other-metrics-sample-{index}.json"
        )
        for key in other_metrics:
            if key not in result:
                result[key] = {
                    "kendalltau": [],
                    "spearmanr": [],
                    "pearsonr": [],
                    "rmse": [],
                }
            result[key]["kendalltau"].append(other_metrics[key][0])
            result[key]["spearmanr"].append(other_metrics[key][1])
            result[key]["pearsonr"].append(other_metrics[key][2])
            result[key]["rmse"].append(other_metrics[key][3])

        file_list = []
        for model in model_temperature_map:
            for method in method_map:
                temperature = model_temperature_map[model]
                file_list.append(f"{model}-{method}-{temperature}")

        for file_name in file_list:
            correlation = calculate_correlation(
                f"output/conala/{file_name}-sample-{index}.json"
            )
            if file_name not in result:
                result[file_name] = {
                    "kendalltau": [],
                    "spearmanr": [],
                    "pearsonr": [],
                    "invalid_cnt": [],
                    "total_cnt": [],
                    "rmse": [],
                }
            result[file_name]["kendalltau"].append(correlation["kendalltau"])
            result[file_name]["spearmanr"].append(correlation["spearmanr"])
            result[file_name]["pearsonr"].append(correlation["pearsonr"])
            result[file_name]["invalid_cnt"].append(correlation["invalid_cnt"])
            result[file_name]["total_cnt"].append(correlation["total_cnt"])
            result[file_name]["rmse"].append(correlation["rmse"])

    return result


def print_example_table(data):
    def add_bold(string):
        return "\\textbf{" + string + "}"

    max_kendalltau = -1
    max_spearmanr = -1
    max_pearsonr = -1

    for metric in existed_metric_map:
        name = metric
        average_kendalltau = np.nanmean(extend(data[name]["kendalltau"]))
        average_spearmanr = np.nanmean(extend(data[name]["spearmanr"]))
        average_pearsonr = np.nanmean(extend(data[name]["pearsonr"]))

        max_kendalltau = max(max_kendalltau, average_kendalltau)
        max_spearmanr = max(max_spearmanr, average_spearmanr)
        max_pearsonr = max(max_pearsonr, average_pearsonr)
        print(
            f"{existed_metric_map[name]} & {average_kendalltau:.3f} & {average_spearmanr:.3f} \\\\"
        )

    max_kendalltau_map = {}
    max_spearmanr_map = {}
    max_pearsonr_map = {}

    for model in model_temperature_map:
        max_kendalltau_map[model] = max_kendalltau
        max_spearmanr_map[model] = max_spearmanr
        max_pearsonr_map[model] = max_pearsonr

    for model in model_temperature_map:
        for method in method_map:
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            data[name]["average_kendalltau"] = np.nanmean(
                extend(data[name]["kendalltau"])
            )
            data[name]["average_spearmanr"] = np.nanmean(
                extend(data[name]["spearmanr"])
            )
            data[name]["average_pearsonr"] = np.nanmean(extend(data[name]["pearsonr"]))

            max_kendalltau_map[model] = max(
                max_kendalltau_map[model], data[name]["average_kendalltau"]
            )
            max_spearmanr_map[model] = max(
                max_spearmanr_map[model], data[name]["average_spearmanr"]
            )
            max_pearsonr_map[model] = max(
                max_pearsonr_map[model], data[name]["average_pearsonr"]
            )

    for model in model_temperature_map:
        print(
            "\\hline\n\\headercolorlong\n\\multicolumn{4}{c}"
            + f"{{\\textbf{{{model_name_map[model]}}}}}\\\\\n\\tableskip"
        )
        for method in method_map:
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            if data[name]["average_kendalltau"] == max_kendalltau_map[model]:
                kendalltau_string = add_bold(f"{data[name]['average_kendalltau']:.3f}")
            else:
                kendalltau_string = f"{data[name]['average_kendalltau']:.3f}"

            if data[name]["average_spearmanr"] == max_spearmanr_map[model]:
                spearmanr_string = add_bold(f"{data[name]['average_spearmanr']:.3f}")
            else:
                spearmanr_string = f"{data[name]['average_spearmanr']:.3f}"
            if data[name]["average_pearsonr"] == max_pearsonr_map[model]:
                pearsonr_string = add_bold(f"{data[name]['average_pearsonr']:.3f}")
            else:
                pearsonr_string = f"{data[name]['average_pearsonr']:.3f}"

            print(
                f"{method_map[method]} & {kendalltau_string} & {spearmanr_string} \\\\"
            )
            if method == "1-2":
                print("\\midrule")


def print_invalid_rate(data):
    print("\n------------ Invalid Rate Table ------------\n")
    for model in model_temperature_map:
        print(
            "\\hline\n\\headercolorlong\n\\multicolumn{4}{c}"
            + f"{{\\textbf{{{model_name_map[model]}}}}}\\\\\n\\tableskip"
        )
        for method in method_map:
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            invalid_cnt = np.sum(data[name]["invalid_cnt"])
            total_cnt = np.sum(data[name]["total_cnt"])
            print(
                f"{method_map[method]} & {invalid_cnt / total_cnt * 100:.3f}\\% & {invalid_cnt} & {total_cnt} \\\\"
            )
    print("\n--------------------------------------------")


def generate_invalid_rate_table(data):
    print("Invalid Rate Table")
    average_invalid_rate_map = {}
    for model in model_temperature_map:
        for method in method_map:
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            invalid_cnt = np.sum(data[name]["invalid_cnt"])
            total_cnt = np.sum(data[name]["total_cnt"])
            average_invalid_rate_map[f"{model}-{method}"] = invalid_cnt / total_cnt

    for method in method_map:
        print(f"{method_map[method]}", end="")
        for model in model_temperature_map:
            name = f"{model}-{method}"
            print(f" & {100 * average_invalid_rate_map[name]:.2f}", end="")
        print(" \\\\")


def generate_rmse_table(data):
    print("RMSE Table")
    average_rmse_map = {}

    for metric in existed_metric_map:
        name = metric
        rmse = data[name]["rmse"]
        print(f"{existed_metric_map[name]}", end="")
        print(f" & {np.nanmean(rmse):.2f} \\\\")

    for model in model_temperature_map:
        for method in method_map:
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            rmse = np.nanmean(data[name]["rmse"])
            average_rmse_map[f"{model}-{method}"] = rmse

    for model in model_temperature_map:
        print(
            "\\hline\n\\headercolorlong\n\\multicolumn{7}{c}"
            + f"{{\\textbf{{{model_name_map[model]}}}}}\\\\\n\\tableskip"
        )
        for method in method_map:
            name = f"{model}-{method}"
            print(f"{method_map[method]}", end="")
            print(f" & {average_rmse_map[name]:.2f} \\\\")


def main():
    print_data = calculate()
    print_example_table(print_data)
    print("\n\n----------------------------------------\n\n", end="")
    print_invalid_rate(print_data)
    generate_invalid_rate_table(print_data)
    print("\n\n----------------------------------------\n\n", end="")
    generate_rmse_table(print_data)


if __name__ == "__main__":
    main()
