import json
import re
from scipy import stats

test_cases = [
    "cpp-small-validation",
    "java-small-validation",
    "js-small-validation",
    "python-small-validation",
]

files = [
    "gpt-3.5-turbo-0613-1-4-0.0-sample-0.json",
    "gpt-3.5-turbo-0613-1-5-0.0-sample-0.json",
]


def extend(array):
    """
    Extend a list of lists to a list
    Examples:
        [[1, 2], [3, 4]] -> [1, 2, 3, 4]
    """
    return [item for sublist in array for item in sublist]


def calculate_correlation(data):
    references, predictions = [], []

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


def answer_to_score(answer, minor_score, major_score, fatal_score):
    def parse_json_list(s: str) -> list:
        json_list_match = re.search(r"\[\s*?\{.*?\}\s*?\]", s, re.DOTALL)
        if json_list_match:
            json_list_str = json_list_match.group(0)
            return json.loads(json_list_str)
        raise ValueError("Invalid JSON string")

    def parse_json_dict(s: str) -> dict:
        json_list_match = re.search(r"\{.*?\}", s, re.DOTALL)
        if json_list_match:
            json_list_str = json_list_match.group(0)
            return json.loads(json_list_str)
        raise ValueError("Invalid JSON string")

    try:
        json_list = parse_json_list(answer)
    except:
        try:
            json_list = [parse_json_dict(answer)]
        except:
            return -1

    score = 100
    for item in json_list:
        try:
            if item["severity"].lower() == "fatal":
                score -= fatal_score
            elif item["severity"].lower() == "major":
                score -= major_score
            elif item["severity"].lower() == "minor":
                score -= minor_score
            elif (
                item["mistake"].lower() == "none"
                or item["severity"].lower() == "none"
                or item["severity"] == ""
            ):
                pass
            else:
                raise ValueError("Invalid severity")
        except Exception:
            return -1
    return max(score, 0) / 100


def get_correlation(minor_score, major_score, fatal_score):
    correlation = {}
    for file in files:
        correlation[file] = {}
        for test_case in test_cases:
            with open(f"output/humaneval/{test_case}/{file}", "r") as f:
                data = json.load(f)
            for item in data["data"]:
                item["code_gpt_score"]["code_gpt_score"] = answer_to_score(
                    item["code_gpt_score"]["comparison"],
                    minor_score,
                    major_score,
                    fatal_score,
                )
            correlation[file][test_case] = {
                "kendalltau": calculate_correlation(data)[0],
                "spearmanr": calculate_correlation(data)[1],
                "invalid_cnt": calculate_correlation(data)[2],
                "total_cnt": calculate_correlation(data)[3],
            }
    return correlation


def sweep():
    max_kendalltau = 0
    max_spearmanr = 0
    max_kendalltau_tuple = (0, 0, 0)
    max_spearmanr_tuple = (0, 0, 0)
    for minor_score in range(5, 101, 5):
        for major_score in range(minor_score + 5, 101, 5):
            for fatal_score in range(major_score + 5, 101, 5):
                print(f"minor_score: {minor_score}, major_score: {major_score}, fatal_score: {fatal_score}")
                correlation = get_correlation(minor_score, major_score, fatal_score)
                for file in files:
                    average_kendalltau = 0
                    average_spearmanr = 0
                    for test_case in test_cases:
                        average_kendalltau += correlation[file][test_case]["kendalltau"]
                        average_spearmanr += correlation[file][test_case]["spearmanr"]
                    average_kendalltau /= len(test_cases)
                    average_spearmanr /= len(test_cases)
                    if average_kendalltau > max_kendalltau:
                        max_kendalltau = average_kendalltau
                        max_kendalltau_tuple = (minor_score, major_score, fatal_score)
                    if average_spearmanr > max_spearmanr:
                        max_spearmanr = average_spearmanr
                        max_spearmanr_tuple = (minor_score, major_score, fatal_score)

    print(f"max kendalltau: {max_kendalltau}")
    print(f"max kendalltau tuple: {max_kendalltau_tuple}")
    print(f"max spearmanr: {max_spearmanr}")
    print(f"max spearmanr tuple: {max_spearmanr_tuple}")


sweep()
