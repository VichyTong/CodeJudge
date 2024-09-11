import json
import os
import argparse

def combine_json_files_to_jsonl(directory, output_filename, language):
    """
    Combine multiple JSON files in the specified directory into a single JSONL file.

    Args:
    - directory (str): Directory containing the JSON files.
    - output_filename (str): Name of the output JSONL file.
    """

    with open(output_filename, 'w') as jsonl_file:
        # Iterate over all .json files in the directory
        for filename in sorted(os.listdir(directory)):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                print(filepath)
                with open(filepath, 'r') as json_file:
                    data = json.load(json_file)
                    for code in data["generation"]:
                        out = {}
                        if language == "cpp":
                            out["generation"] = code + "\n}"
                        elif language == "java":
                            out["generation"] = code + "\n    }\n}"
                        else:
                            out["generation"] = code
                        out["prompt"] = data["prompt"]
                        out["task_id"] = data["task_id"]
                        jsonl_file.write(json.dumps(out) + '\n')

    print(f"Combined JSON files into {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, required=True)
    parser.add_argument('--output_filename', type=str, required=True)
    parser.add_argument('--language', type=str, required=True)
    args = parser.parse_args()
    combine_json_files_to_jsonl(args.directory, args.output_filename, args.language)
