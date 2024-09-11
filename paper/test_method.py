import os
import sys
import json
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code_model_score import form_filling, answer_to_score
from evaluation.humaneval.prompts import single_step_prompt, dual_step_prompt


type_map = {
    2: "error_level",
    3: "error_level",
    4: "0_to_4_score_functional_correctness",
    5: "0_to_4_score_functional_correctness",
}


def single_step_workflow(program, canonical_solution, problem):
    for i in range(2, 6):
        code_gpt_answer = form_filling(
            "gpt-3.5-turbo-0613",
            single_step_prompt[i],
            tokenizer=None,
            pipeline=None,
            temperature=0,
            code1=program,
            code2=canonical_solution,
            problem=problem,
        )
        
        code_gpt_score = answer_to_score(code_gpt_answer, type_map[i])
        print(code_gpt_score, end=" ")


def dual_step_workfow(program, canonical_solution, problem):
    for i in range(2):
        nl_mistakes = form_filling(
            "gpt-3.5-turbo-0613",
            dual_step_prompt["compare_prompt"][i],
            None,
            None,
            temperature=0,
            code1=program,
            code2=canonical_solution,
            problem=problem,
        )
            
        code_gpt_answer = form_filling(
            "gpt-3.5-turbo-0613",
            dual_step_prompt["analyze_prompt"][0],
            None,
            None,
            temperature=0,
            mistakes=nl_mistakes,
        )

        code_gpt_score = answer_to_score(code_gpt_answer, "bool")
        print(float(code_gpt_score), end=" ")

partially_correct_prediction = """\
def anti_shuffle(s):
    return ' '.join([sorted(list(i)) for i in s.split(' ')])
"""

lexically_different_prediction = """\
def anti_shuffle(s):
    return ' '.join([''.join(sorted(list(word))) for word in s.split(' ')])
"""
semantically_different_prediction = """\
def anti_shuffle(s):
    word_list = []
    current_word = ""
    for i in range(len(s)):
        if s[i] != " ":
            current_word += s[i]
        else:
            word_list.append("".join(sorted(list(current_word))))
            current_word = ""
    word_list.append("".join(sorted(list(current_word))))
    return ' '.join(word_list)
"""

totally_wrong_prediction = """\
def anti_shuffle(s):
    pass
"""

predictions = [
    partially_correct_prediction,
    totally_wrong_prediction,
    lexically_different_prediction,
    semantically_different_prediction,
]

reference = """\
def anti_shuffle(s):
    return ' '.join([''.join(sorted(list(i))) for i in s.split(' ')])
"""

problem = """\
Alphabetize letters in each word of a sentence, keeping the words and spaces in the same order.
"""

for i, prediction in enumerate(predictions):
    print(f"prediction {i}: ", end="")
    single_step_workflow(prediction, reference, problem)
    dual_step_workfow(prediction, reference, problem)
    print("")
