import json
import argparse
import os

def calculate_correlation(file_name):
    references, predictions = [], []
    with open(file_name, "r") as f:
        data = json.load(f)

    invalid_cnt = 0
    correct_cnt = 0
    for index, d in enumerate(data["data"]):
        if d["code_gpt_score"]["code_gpt_score"] == -1.0:
            invalid_cnt += 1
            continue
        if float(d["pass"]) == float(d["code_gpt_score"]["code_gpt_score"]):
            correct_cnt += 1
        else:
            print(index, end=" ")
    return correct_cnt, invalid_cnt, len(data["data"])


def print_accuracy(file_name):
    print(file_name.split("/")[-1])
    correct_cnt, invalid_cnt, total_cnt = calculate_correlation(file_name)
    print("correct_cnt: {}/{} = {:.2f}%".format(correct_cnt, total_cnt, correct_cnt/total_cnt*100))
    print("invalid_cnt: {}/{}".format(invalid_cnt, total_cnt))

def find_files_with_substring(directory, substring):
    # List to hold files that match the criterion
    matching_files = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        # Check each file name for the substring
        for file in files:
            if substring in file:
                # Add the file path to the list if it contains the substring
                matching_files.append(os.path.join(root, file))
    
    return matching_files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_case", type=str)
    args = parser.parse_args()
    test_case = args.test_case

    matching_files = find_files_with_substring(f"output/humaneval/{test_case}", ".json")
    matching_files.sort()
    for file_name in matching_files:
        print_accuracy(f"{file_name}")


if __name__ == "__main__":
    main()
