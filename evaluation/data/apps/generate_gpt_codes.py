# Modified from https://github.com/hendrycks/apps/blob/main/eval/generate_gpt_codes.py


"""
Run a tranined model to generate Python code.
"""

import io
import json
import logging
import math
import random
import numpy as np
import os
import pprint
import sys
import time
import torch

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from code_model_score import openai_request, form_filling, load_model

from reindent import run as run_reindent

# for timing and debugging
from datetime import datetime, date
from tqdm import tqdm


def reindent_code(codestr):
    """
    Given code string, reindent it in the same way that the
    Github dataset was indented
    """
    codestr = io.StringIO(codestr)
    ret = io.StringIO()

    run_reindent(
        codestr,
        ret,
        config={
            "dry-run": False,
            "help": False,
            "to": 10,
            "from": -1,
            "tabs": True,
            "encoding": "utf-8",
            "is-tabs": False,
            "tabsize": 10,
            "all-tabs": False,
        },
    )

    return ret.getvalue()


def generate_prompt(
    args, test_case_path, prompt_path, solutions_path, starter_path=None
):
    _input = "\nQUESTION:\n"
    with open(prompt_path, "r") as f:
        data = f.readlines()
        data = "".join(data)
    _input += data
    if starter_path != None:
        with open(starter_path, "r") as f:
            data = f.readlines()
            data = "".join(data)
            data = "\n" + data  # + "\n"
        _input += data
    else:
        # _input += "\n\n"
        pass

    with open(test_case_path, "r") as f:
        data = json.load(f)
    if not data.get("fn_name"):
        _input += "\nUse Standard Input format"  # \n"
    else:
        _input += "\nUse Call-Based format"  # \n"

    return _input


def main(args):

    argsdict = vars(args)
    print(pprint.pformat(argsdict))

    with open(args.test_loc, "r") as f:
        problems = json.load(f)
    problems = sorted(problems)  # Pin some ordering

    gpt_codes = {}
    if not os.path.exists(args.save):
        os.makedirs(args.save, exist_ok=True)
    if not args.end:
        codes_loc = os.path.join(args.save, f"all_codes.json")
    else:
        codes_loc = os.path.join(args.save, f"{args.start}-{args.end}_codes.json")

    # Only do the problems that are specified.
    if args.index:
        problems = [problems[args.index]]
    else:
        if args.start > len(problems) or args.start < 0:
            print(f"start index {args.start} > number of problems {len(problems)}")
            return
        start = args.start
        if args.end is None or args.end > len(problems):
            end = len(problems)
        else:
            end = args.end
        problems = problems[start:end]

    # main eval loop
    for index, problem in enumerate(tqdm(problems)):
        prob_path = os.path.join(args.root, problem)
        if args.debug:
            print(f"problem path = {prob_path}")

        test_case_path = os.path.join(prob_path, "input_output.json")
        prompt_path = os.path.join(prob_path, "question.txt")
        starter_path = os.path.join(prob_path, "starter_code.py")
        solutions_path = os.path.join(prob_path, "solutions.json")
        if not os.path.exists(starter_path):
            starter_path = None
        if not os.path.exists(test_case_path) or not os.path.exists(prompt_path):
            continue

        # Read the question in
        prompt_text = generate_prompt(
            args, test_case_path, prompt_path, solutions_path, starter_path
        )
        if args.debug:
            print("PROMPT_TEXT:")
            print(prompt_text)

        # Feed this into the model.
        start = time.time()
        try:
            message = [
                {
                    "role": "system",
                    "content": prompt_text
                    + "\nDirectly output the code snippet between ```python and ```.",
                },
                {
                    "role": "assistant",
                    "content": "```python\n",
                },
            ]
            output_str = openai_request(message, "gpt-4o", temperature=0).strip()
            if "```python\n" in output_str:
                output_str = output_str.split("```python\n")[1]
            if "```\npython\n" in output_str:
                output_str = output_str.split("```\npython\n")[1]
            if "```\n" in output_str:
                output_str = output_str.split("```\n")[1]
            if "\n```" in output_str:
                output_str = output_str.split("\n```")[0]
            # print(output_str)
            output_str = output_str.strip()
        except Exception as e:
            print("Unexpected exception in generating solution")
            print(e)
            # Default to empty string on errors
            output_str = ""
        end = time.time()

        # Save the generated sol
        gpt_codes[index + args.start] = output_str

        if args.debug:
            print(f"Generation time: {end - start}")
            print(f"Generated output string:")
            print(output_str)
            print("------------------------------------------------------------")

    with open(codes_loc, "w") as f:
        json.dump(gpt_codes, f)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run a tranined model to generate Python code."
    )
    parser.add_argument("-t", "--test_loc", default="test.json", type=str)
    parser.add_argument(
        "-r", "--root", default="APPS/test", type=str, help="where the data is stored."
    )
    parser.add_argument("-s", "--start", default=0, type=int)
    parser.add_argument("-e", "--end", default=None, type=int)
    parser.add_argument("-i", "--index", default=None, type=int)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--save", type=str, default="./results")

    args = parser.parse_args()

    main(args)
