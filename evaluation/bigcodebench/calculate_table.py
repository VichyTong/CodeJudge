import json
import os

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


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
    correct_cnt = 0
    # with open("data/bigcodebench/results/all_results.json", "r") as f:
    #     all_results = json.load(f)

    if "-1-2-" in file_name or "-1-3-" in file_name:
        is_ice = True
    else:
        is_ice = False

    for index, d in enumerate(data["data"]):
        if d["code_gpt_score"]["code_gpt_score"] == -1.0:
            invalid_cnt += 1
            if is_ice:
                if d["pass"]:
                    d["code_gpt_score"]["code_gpt_score"] = 0.0
                else:
                    d["code_gpt_score"]["code_gpt_score"] = 4.0
            else:
                if d["pass"]:
                    d["code_gpt_score"]["code_gpt_score"] = 0.0
                else:
                    d["code_gpt_score"]["code_gpt_score"] = 1.0

        if is_ice:
            predict = 1.0 if d["code_gpt_score"]["code_gpt_score"] == 4.0 else 0.0
            if d["pass"] == predict:
                correct_cnt += 1
        else:
            if d["pass"] == d["code_gpt_score"]["code_gpt_score"]:
                correct_cnt += 1

        # test_case_correct_count = 0
        # for result in all_results[str(index)][0]:
        #     if result == True:
        #         test_case_correct_count += 1
        # test_case_accuracy = test_case_correct_count / len(all_results[str(index)][0])
        # references.append([test_case_accuracy])
        references.append([float(d["pass"])])
        predictions.append([float(d["code_gpt_score"]["code_gpt_score"])])

    kendalltau = stats.kendalltau(extend(references), extend(predictions)).statistic
    spearmanr = stats.spearmanr(extend(references), extend(predictions)).statistic

    if not is_ice:
        accuracy = accuracy_score(extend(references), extend(predictions))
        precision = precision_score(extend(references), extend(predictions), zero_division=0)
        recall = recall_score(extend(references), extend(predictions), zero_division=0)
        f1 = f1_score(extend(references), extend(predictions), zero_division=0)

        result = {
            "kendalltau": kendalltau,
            "spearmanr": spearmanr,
            "invalid_cnt": invalid_cnt,
            "total_cnt": len(data["data"]),
            "correct_cnt": correct_cnt,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }
    else:
        result = {
            "kendalltau": kendalltau,
            "spearmanr": spearmanr,
            "invalid_cnt": invalid_cnt,
            "total_cnt": len(data["data"]),
            "correct_cnt": correct_cnt,
        }
    print(file_name)
    print(json.dumps(result, indent=4))
    print(len(extend(references)), len(extend(predictions)))
    return result


def calculate_other_correlation(file_name):
    references = []
    predictions = {
        "bleu": [],
        "rougeL": [],
        "meteor": [],
        "chrf": [],
        "codebleu": [],
        "ruby": [],
        "CodeBERTScore_f1": [],
        "CodeBERTScore_f3": [],
    }

    with open(file_name, "r") as f:
        data = json.load(f)

    for item in data:
        references.append([float(item["pass"])])
        predictions["bleu"].append([float(item["bleu"])])
        predictions["rougeL"].append([float(item["rougel"])])
        predictions["meteor"].append([float(item["meteor"])])
        predictions["chrf"].append([float(item["chrf"])])
        predictions["codebleu"].append([float(item["codebleu"])])
        predictions["ruby"].append([float(item["ruby"])])
        predictions["CodeBERTScore_f1"].append([item["code_bert_score_f1"]])
        predictions["CodeBERTScore_f3"].append([item["code_bert_score_f3"]])

    result = {}

    for key in predictions:
        kendalltau = stats.kendalltau(
            extend(references), extend(predictions[key])
        ).statistic
        spearmanr = stats.spearmanr(
            extend(references), extend(predictions[key])
        ).statistic
        result[key] = {
            "kendalltau": kendalltau,
            "spearmanr": spearmanr,
            "invalid_cnt": 0,
            "total_cnt": len(data),
        }

    return result


test_case_list = [
    "codellama--CodeLlama-13b-Instruct-hf",
]

existed_metric_map = {
    "bleu": "BLEU",
    "rougeL": "ROUGE-L",
    "meteor": "METEOR",
    "chrf": "chrF",
    "codebleu": "CodeBLEU",
    "ruby": "RUBY",
    "CodeBERTScore_f1": "CodeBERTScore$_{\\text{F}_1}$",
    "CodeBERTScore_f3": "CodeBERTScore$_{\\text{F}_3}$",
}

model_temperature_map = {
    "CodeLlama-34b-Instruct": "0.4",
    "Meta-Llama-3-8B-Instruct": "0.4",
    "Meta-Llama-3-70B-Instruct": "0.4",
    "gpt-3.5-turbo-1106": "0.0",
}

model_name_map = {
    "CodeLlama-34b-Instruct": "CodeLlama-Instruct-34B",
    "Meta-Llama-3-8B-Instruct": "Meta-Llama-3-8B-Instruct",
    "Meta-Llama-3-70B-Instruct": "Meta-Llama-3-70B-Instruct",
    "gpt-3.5-turbo-1106": "GPT-3.5-Turbo-1106",
}

basic_method_map = {
    "1-1": "\\bool{}",
    "1-0": "\\bool{} w/o \\reference{}",
    "1-3": "ICE-Score",
    "1-2": "ICE-Score w/o \\reference{}",
    "2-0-1": "\\citeeval{}",
    "2-0-0": "\\citeeval{} w/o \\reference{}",
    # "1-5": "\\codemistake{}",
    # "1-4": "\\codemistake{} w/o \\reference{}",
}

codellama_method_map = {
    "1-1": "\\bool{}",
    "1-0": "\\bool{} w/o \\reference{}",
    "1-3": "ICE-Score",
    "1-2": "ICE-Score w/o \\reference{}",
    "2-0-1": "\\codedual{}",
    "2-0-0": "\\codedual{} w/o \\reference{}",
    # "1-5": "\\codemistake{}",
    # "1-4": "\\codemistake{} w/o \\reference{}",
}


def get_method_map(model):
    if model.startswith("CodeLlama"):
        return codellama_method_map
    else:
        return basic_method_map


def print_table(data):
    for test_case in test_case_list:

        def mark_data(
            data,
            name,
            highest_kendalltau,
            highest_spearmanr,
        ):
            if data[test_case][name]["average_kendalltau"] == highest_kendalltau:
                data[test_case][name]["kendalltau_string"] = (
                    "\\textbf{"
                    + f"{data[test_case][name]['average_kendalltau']:.3f}"
                    + "}"
                )
            else:
                data[test_case][name][
                    "kendalltau_string"
                ] = f"{data[test_case][name]['average_kendalltau']:.3f}"

            if data[test_case][name]["average_spearmanr"] == highest_spearmanr:
                data[test_case][name]["spearmanr_string"] = (
                    "\\textbf{"
                    + f"{data[test_case][name]['average_spearmanr']:.3f}"
                    + "}"
                )
            else:
                data[test_case][name][
                    "spearmanr_string"
                ] = f'{data[test_case][name]["average_spearmanr"]:.3f}'

            std_kendalltau = data[test_case][name]["std_kendalltau"]
            std_spearmanr = data[test_case][name]["std_spearmanr"]
            data[test_case][name]["kendalltau_string_full"] = (
                data[test_case][name]["kendalltau_string"]
                + "$_{\pm "
                + f"{std_kendalltau:.2f}"
                + "}$"
            )
            data[test_case][name]["spearmanr_string_full"] = (
                data[test_case][name]["spearmanr_string"]
                + "$_{\pm "
                + f"{std_spearmanr:.2f}"
                + "}$"
            )
            return data

        for model in model_temperature_map:
            k_list = []
            s_list = []

            for metric in existed_metric_map:
                name = metric
                kendalltau = data[test_case][name]["average_kendalltau"]
                spearmanr = data[test_case][name]["average_spearmanr"]
                k_list.append(kendalltau)
                s_list.append(spearmanr)
            for method in get_method_map(model):
                temperature = model_temperature_map[model]
                name = f"{model}-{method}-{temperature}"
                kendalltau = data[test_case][name]["average_kendalltau"]
                spearmanr = data[test_case][name]["average_spearmanr"]
                k_list.append(kendalltau)
                s_list.append(spearmanr)

            highest_kendalltau = max(k_list)
            highest_spearmanr = max(s_list)

            for metric in existed_metric_map:
                name = metric
                data = mark_data(
                    data,
                    name,
                    highest_kendalltau,
                    highest_spearmanr,
                )
            for method in get_method_map(model):
                temperature = model_temperature_map[model]
                name = f"{model}-{method}-{temperature}"
                data = mark_data(
                    data,
                    name,
                    highest_kendalltau,
                    highest_spearmanr,
                )
            print(test_case, model, highest_kendalltau, highest_spearmanr)

    average_kendalltau_map = {}
    average_spearmanr_map = {}
    for metric in existed_metric_map:
        name = metric
        average_kendalltau = 0
        average_spearmanr = 0
        for test_case in test_case_list:
            average_kendalltau += data[test_case][name]["average_kendalltau"]
            average_spearmanr += data[test_case][name]["average_spearmanr"]
        average_kendalltau /= len(test_case_list)
        average_spearmanr /= len(test_case_list)

        average_kendalltau_map[name] = average_kendalltau
        average_spearmanr_map[name] = average_spearmanr

    for model in model_temperature_map:
        for method in get_method_map(model):
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            average_kendalltau = 0
            average_spearmanr = 0
            for test_case in test_case_list:
                temperature = model_temperature_map[model]
                name = f"{model}-{method}-{temperature}"
                average_kendalltau += data[test_case][name]["average_kendalltau"]
                average_spearmanr += data[test_case][name]["average_spearmanr"]
            average_kendalltau /= len(test_case_list)
            average_spearmanr /= len(test_case_list)

            average_kendalltau_map[name] = average_kendalltau
            average_spearmanr_map[name] = average_spearmanr

    first_average_kendalltau = max(average_kendalltau_map.values())
    first_average_spearmanr = max(average_spearmanr_map.values())
    second_average_kendalltau = sorted(average_kendalltau_map.values())[-2]
    second_average_spearmanr = sorted(average_spearmanr_map.values())[-2]

    average_kendalltau_string_map = {}
    average_spearmanr_string_map = {}

    for metric in existed_metric_map:
        name = metric
        if average_kendalltau_map[name] == first_average_kendalltau:
            average_kendalltau_string_map[name] = (
                "\\textbf{" + f"{average_kendalltau_map[name]:.3f}" + "}"
            )
        elif average_kendalltau_map[name] == second_average_kendalltau:
            average_kendalltau_string_map[name] = f"{average_kendalltau_map[name]:.3f}"
        else:
            average_kendalltau_string_map[name] = f"{average_kendalltau_map[name]:.3f}"

        if average_spearmanr_map[name] == first_average_spearmanr:
            average_spearmanr_string_map[name] = (
                "\\textbf{" + f"{average_spearmanr_map[name]:.3f}" + "}"
            )
        elif average_spearmanr_map[name] == second_average_spearmanr:
            average_spearmanr_string_map[name] = f"{average_spearmanr_map[name]:.3f}"
        else:
            average_spearmanr_string_map[name] = f"{average_spearmanr_map[name]:.3f}"

    for model in model_temperature_map:
        for method in get_method_map(model):
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            if average_kendalltau_map[name] == first_average_kendalltau:
                average_kendalltau_string_map[name] = (
                    "\\textbf{" + f"{average_kendalltau_map[name]:.3f}" + "}"
                )
            elif average_kendalltau_map[name] == second_average_kendalltau:
                average_kendalltau_string_map[name] = (
                    f"{average_kendalltau_map[name]:.3f}"
                )
            else:
                average_kendalltau_string_map[name] = (
                    f"{average_kendalltau_map[name]:.3f}"
                )

            if average_spearmanr_map[name] == first_average_spearmanr:
                average_spearmanr_string_map[name] = (
                    "\\textbf{" + f"{average_spearmanr_map[name]:.3f}" + "}"
                )
            elif average_spearmanr_map[name] == second_average_spearmanr:
                average_spearmanr_string_map[name] = (
                    f"{average_spearmanr_map[name]:.3f}"
                )
            else:
                average_spearmanr_string_map[name] = (
                    f"{average_spearmanr_map[name]:.3f}"
                )

    print(
        "\\headercolorlong\n\\multicolumn{3}{c}"
        + "{\\textsc{Existing Methods}}\\\\\n\\tableskip"
    )

    for metric in existed_metric_map:
        name = metric
        print(f"{existed_metric_map[name]}", end="")
        for test_case in test_case_list:
            print(f" & {data[test_case][name]['kendalltau_string']}", end="")
            print(f" & {data[test_case][name]['spearmanr_string']}", end="")
        print(f" \\\\")

    for model in model_temperature_map:
        print(
            "\\hline\n\\headercolorlong\n\\multicolumn{3}{c}"
            + f"{{\\textbf{{{model_name_map[model]}}}}}\\\\\n\\tableskip"
        )
        method_map = get_method_map(model)
        for method in method_map:
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            print(f"{method_map[method]}", end="")
            for test_case in test_case_list:
                print(f" & {data[test_case][name]['kendalltau_string']}", end="")
                print(f" & {data[test_case][name]['spearmanr_string']}", end="")
            print(f" \\\\")

    print("---------------------------------------")
    print(
        "\\headercolorlong\n\\multicolumn{3}{c}"
        + "{\\textsc{Existing Methods}}\\\\\n\\tableskip"
    )

    for metric in existed_metric_map:
        name = metric
        print(f"{existed_metric_map[name]}", end="")
        for test_case in test_case_list:
            print(f" & {data[test_case][name]['kendalltau_string_full']}", end="")
            print(f" & {data[test_case][name]['spearmanr_string_full']}", end="")
        print(" \\\\")

    for model in model_temperature_map:
        print(
            "\\hline\n\\headercolorlong\n\\multicolumn{3}{c}"
            + f"{{\\textbf{{{model_name_map[model]}}}}}\\\\\n\\tableskip"
        )
        method_map = get_method_map(model)
        for method in method_map:
            temperature = model_temperature_map[model]
            name = f"{model}-{method}-{temperature}"
            print(f"{method_map[method]}", end="")
            for test_case in test_case_list:
                print(f" & {data[test_case][name]['kendalltau_string_full']}", end="")
                print(f" & {data[test_case][name]['spearmanr_string_full']}", end="")
            print(" \\\\")
            if method == "1-2":
                print("\\midrule")


def calculate():
    result = {}
    # calculate other metrics' correlation
    for test_case in test_case_list:
        result[test_case] = {}
        for index in range(0, 3):
            other_metrics = calculate_other_correlation(
                f"output/bigcodebench/{test_case}/other-metrics-without-prefix-sample-{index}.json"
            )
            for key in other_metrics:
                if key not in result[test_case]:
                    result[test_case][key] = {
                        "kendalltau": [],
                        "spearmanr": [],
                        "invalid_cnt": [],
                        "total_cnt": [],
                        "accuracy": [],
                        "std_accuracy": [],
                    }
                result[test_case][key]["kendalltau"].append(
                    other_metrics[key]["kendalltau"]
                )
                result[test_case][key]["spearmanr"].append(
                    other_metrics[key]["spearmanr"]
                )
                result[test_case][key]["invalid_cnt"].append(
                    other_metrics[key]["invalid_cnt"]
                )
                result[test_case][key]["total_cnt"].append(
                    other_metrics[key]["total_cnt"]
                )

    # calculate LLMs metrics' correlation
    file_list = []
    for model in model_temperature_map:
        for method in get_method_map(model):
            temperature = model_temperature_map[model]
            file_list.append(f"{model}-{method}-{temperature}")

    for test_case in test_case_list:
        for file_name in file_list:
            if "gpt-3.5-turbo" in file_name:
                num = 1
            else:
                num = 3
            for index in range(0, num):
                correlation = calculate_correlation(
                    f"output/bigcodebench/{test_case}/{file_name}-sample-{index}.json"
                )
                if file_name not in result[test_case]:
                    result[test_case][file_name] = {
                        "kendalltau": [],
                        "spearmanr": [],
                        "invalid_cnt": [],
                        "total_cnt": [],
                        "correct_cnt": [],
                    }
                result[test_case][file_name]["kendalltau"].append(
                    correlation["kendalltau"]
                )
                result[test_case][file_name]["spearmanr"].append(
                    correlation["spearmanr"]
                )
                result[test_case][file_name]["invalid_cnt"].append(
                    correlation["invalid_cnt"]
                )
                result[test_case][file_name]["total_cnt"].append(
                    correlation["total_cnt"]
                )
                result[test_case][file_name]["correct_cnt"].append(
                    correlation["correct_cnt"]
                )

    print_data = {}

    for test_case in test_case_list:
        print_data[test_case] = {}
        for key in result[test_case]:
            invalid_rate_list = []
            for index in range(len(result[test_case][key]["invalid_cnt"])):
                invalid_rate_list.append(
                    result[test_case][key]["invalid_cnt"][index]
                    / result[test_case][key]["total_cnt"][index]
                )
            invalid_rate = np.mean(invalid_rate_list)

            accuracy_list = []
            if "correct_cnt" in result[test_case][key]:
                for index in range(len(result[test_case][key]["correct_cnt"])):
                    accuracy_list.append(
                        result[test_case][key]["correct_cnt"][index]
                        / result[test_case][key]["total_cnt"][index]
                    )
            accuracy = np.mean(accuracy_list)
            std_accuracy = np.std(accuracy_list)

            print_data[test_case][key] = {
                "average_kendalltau": np.mean(result[test_case][key]["kendalltau"]),
                "average_spearmanr": np.mean(result[test_case][key]["spearmanr"]),
                "std_kendalltau": np.std(result[test_case][key]["kendalltau"]),
                "std_spearmanr": np.std(result[test_case][key]["spearmanr"]),
                "invalid_rate": invalid_rate,
                "accuracy": accuracy,
                "std_accuracy": std_accuracy,
            }

    return print_data


def generate_invalid_rate_table(data):
    print("\n------------- Invalid Rate Table -------------\n")
    average_invalid_rate_map = {}
    for model in model_temperature_map:
        for method in get_method_map(model):
            average_invalid_rate = 0
            for test_case in test_case_list:
                temperature = model_temperature_map[model]
                name = f"{model}-{method}-{temperature}"
                invalid_rate = data[test_case][name]["invalid_rate"]
                average_invalid_rate += invalid_rate
            average_invalid_rate /= len(test_case_list)
            average_invalid_rate_map[f"{model}-{method}"] = average_invalid_rate

    for method in basic_method_map:
        print(f"{basic_method_map[method]}", end="")
        for model in model_temperature_map:
            name = f"{model}-{method}"
            print(f" & {100 * average_invalid_rate_map[name]:.2f}", end="")
        print(" \\\\")
    print("\n----------------------------------------------\n")


accuracy_basic_method_map = {
    "1-1": "\\bool{}",
    "1-0": "\\bool{} w/o \\reference{}",
    "1-3": "ICE-Score",
    "1-2": "ICE-Score w/o \\reference{}",
    "2-0-1": "\\codedual{}",
    "2-0-0": "\\codedual{} w/o \\reference{}",
}

accuracy_codellama_method_map = {
    "1-1": "\\bool{}",
    "1-0": "\\bool{} w/o \\reference{}",
    "1-3": "ICE-Score",
    "1-2": "ICE-Score w/o \\reference{}",
    "2-0-1": "\\codedual{}",
    "2-0-0": "\\codedual{} w/o \\reference{}",
}


def get_accuracy_method_map(model):
    if model.startswith("CodeLlama"):
        return accuracy_codellama_method_map
    else:
        return accuracy_basic_method_map


def generate_accuracy_table(data):
    print(">>> Accuracy Table")
    accuracy_map = {}
    std_accuracy_map = {}

    for model in model_temperature_map:
        accuracy_method_map = get_accuracy_method_map(model)
        for method in accuracy_method_map:
            for test_case in test_case_list:
                temperature = model_temperature_map[model]
                name = f"{model}-{method}-{temperature}"
                accuracy = data[test_case][name]["accuracy"]
                std_accuracy = data[test_case][name]["std_accuracy"]

                if f"{model}-{method}" not in accuracy_map:
                    accuracy_map[f"{model}-{method}"] = []
                accuracy_map[f"{model}-{method}"].append(accuracy)

                if f"{model}-{method}" not in std_accuracy_map:
                    std_accuracy_map[f"{model}-{method}"] = []
                std_accuracy_map[f"{model}-{method}"].append(std_accuracy)

    for model in model_temperature_map:
        print(
            "\\headercolorlong\n\\multicolumn{2}{c}"
            + f"{{\\textbf{{{model_name_map[model]}}}}}\\\\\n\\tableskip"
        )
        accuracy_method_map = get_accuracy_method_map(model)
        for method in accuracy_method_map:
            print(f"{accuracy_method_map[method]}", end="")
            name = f"{model}-{method}"
            average_accuracy = np.mean(accuracy_map[name])
            for accuracy in accuracy_map[name]:
                print(f" & {100 * accuracy:.2f}", end="")
            print(f" \\\\")
    print("")
    print("----------------- FULL TABLE -----------------")
    print("")
    for model in model_temperature_map:
        print(
            "\hline\n\\headercolorlong\n\\multicolumn{2}{c}"
            + f"{{\\textbf{{{model_name_map[model]}}}}}\\\\\n\\tableskip"
        )
        accuracy_method_map = get_accuracy_method_map(model)
        for method in accuracy_method_map:
            print(f"{accuracy_method_map[method]}", end="")
            name = f"{model}-{method}"
            average_accuracy = np.mean(accuracy_map[name])

            for index, accuracy in enumerate(accuracy_map[name]):
                std = std_accuracy_map[name][index]
                print(
                    f" & {100 * accuracy:.2f}" + "$_{\pm " + f"{std:.2f}" + "}$", end=""
                )

            print("\\\\")


def main():
    print_data = calculate()
    print_table(print_data)
    generate_invalid_rate_table(print_data)
    generate_accuracy_table(print_data)


if __name__ == "__main__":
    main()
