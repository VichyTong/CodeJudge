import os
import json
import random
import shutil

def search_and_extract_selected_folders(root_dir):
    # Initialize list to store randomly chosen task indexes
    chosen_indexes = []

    # Get the list of folders in the root directory and sort them
    folders = sorted(filter(lambda x: x.isdigit(), os.listdir(root_dir)))
    # set the seed
    random.seed(42)
    # randomly shuffle the folders
    random.shuffle(folders)

    num_tasks_to_select = 100

    # Reset introductory count
    count = 0

    # Iterate over sorted folders again and select tasks
    for folder_name in folders:
        folder_path = os.path.join(root_dir, folder_name)
        metadata_file = os.path.join(folder_path, "metadata.json")
        solution_file = os.path.join(folder_path, "solutions.json")
        question_file = os.path.join(folder_path, "question.txt")
        if os.path.exists(metadata_file) and os.path.exists(solution_file):
            with open(question_file, "r") as f:
                question = f.read()
                if "[Image]" in question:
                    continue
            count += 1
            if count <= num_tasks_to_select:
                chosen_indexes.append(folder_name)

    # Save chosen task indexes to task_index.json
    with open("test.json", "w") as f:
        json.dump(chosen_indexes, f)

# Provide the root directory
root_directory = "./APPS/test"

# Call the function to search, select, and extract folders
search_and_extract_selected_folders(root_directory)
