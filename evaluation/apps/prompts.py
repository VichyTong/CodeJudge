single_step_prompt = [
    [
        {
            "role": "system",
            "content": """\
Determine the correctness of the code snippet. Output Yes or No. 

Problem Statement:
{{PROBLEM}}

Code Snippet:
{{CODE1}}

Answer (Yes or No only):
""",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
Determine the correctness of the code snippet. Output Yes or No. 

Problem Statement:
{{PROBLEM}}

Reference Solution:
{{CODE2}}

Code Snippet:
{{CODE1}}

Answer (Yes or No only):
""",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
You will be given the code snippet for a problem. 
Your task is to rate the code snippet only on one metric.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Functional Correctness (0-4) - Execution-based quality of the code snippet combined with the problem. The correctness is measured by the all possible unit tests, and the comparison of the reference code. The combination of the code snippet and the problem should pass all the possible tests based on your understanding of the reference code. The length of the code snippet can not determine the correctness. You need to assess the logics line by line.
- A score of 0  (failing all possible test) means that the code snippet is totally incorrect and meaningless.
- A score of 4  (passing all possible test) means that the code snippet is totally correct and can handle all cases.


Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the problem. Check if the code snippet covers all required functionalities of the problem. 
3. Assign a score for functional correctness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{PROBLEM}}

Code Snippet:

{{CODE1}}

Evaluation Form:
Functional Correctness (scores ONLY):
""",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
You will be given the code snippet for a problem. 
Your task is to rate the code snippet only on one metric.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Functional Correctness (0-4) - Execution-based quality of the code snippet combined with the problem. The correctness is measured by the all possible unit tests, and the comparison of the reference code. The combination of the code snippet and the problem should pass all the possible tests based on your understanding of the reference code. The length of the code snippet can not determine the correctness. You need to assess the logics line by line.
- A score of 0  (failing all possible test) means that the code snippet is totally incorrect and meaningless.
- A score of 4  (passing all possible test) means that the code snippet is totally correct and can handle all cases.


Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the reference code. Check if the code snippet covers all required functionalities of the problem, and if it is as good as the reference code. 
3. Assign a score for functional correctness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{PROBLEM}}

Reference Code:

{{CODE2}}

Code Snippet:
{{CODE1}}

Evaluation Form:
Functional Correctness (scores ONLY):
""",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
You will be provided with a problem statement, a code snippet that supposedly addresses the problem, and a catalog of code inconsistencies.

Evaluation Steps:
1. Read the problem statement carefully to identify the functionalities required for the implementation.
2. Read the code snippet and compare it to the problem statement. Check if the code snippet covers the required functionalities.
3. Output your answer in a JSON format list.
    a) If the code snippet is correct, output: [{"inconsistency": "None", "severity": "Negligible"}].
    b) If the code snippet is incorrect, output the identified inconsistencies and their severity according to the catalog of code inconsistencies. For example: [{"inconsistency": "<inconsistency1>", "severity": "<severity1>"}, {"inconsistency": "<inconsistency2>", "severity": "<severity2>"}, ...]

Problem:
{{PROBLEM}}

Code Snippet:
{{CODE1}}

Catalog of Code Inconsistencies:
1. Missing dependency declarations: Negligible
2. No error messages for unexpected input cases: Negligible
3. Inefficiency, unnecessary statements: Negligible
4. Edge case not handled: Small
5. Logic error: Major
6. Function or variable not defined: Fatal
7. Code not completed: Fatal

Evaluation Form:
JSON output (a JSON list only):
""",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
You will be provided with a problem statement, a code snippet that supposedly addresses the problem, a reference solution, and a catalog of code inconsistencies.
 
Evaluation Steps:
1. Read the problem statement and reference solution carefully and identify the required functionalities for the implementation. The reference solution is used to help you understand the problem, do not directly compare the code snippet to the reference code.
2. Read the code snippet and compare it to the problem statement. Check if the code snippet covers the required functionalities.
3. Output your answer in a JSON format list.
    a) If the code snippet is correct, output: [{"inconsistency": "None", "severity": "Negligible"}].
    b) If the code snippet is incorrect, output the identified inconsistencies and their severity according to the catalog of code inconsistencies. For example: [{"inconsistency": "<inconsistency1>", "severity": "<severity1>"}, {"inconsistency": "<inconsistency2>", "severity": "<severity2>"}, ...]

Problem:
{{PROBLEM}}

Reference:
{{CODE2}}

Code Snippet:
{{CODE1}}

Catalog of Code Inconsistencies:
0. Different methods or algorithms: Negligible
1. Missing dependency declarations: Negligible
2. No error messages for unexpected input cases: Negligible
3. Inefficiency, unnecessary statements: Negligible
4. Edge case not handled: Small
5. Logic error: Major
6. Function or variable not defined: Fatal
7. Code not completed: Fatal

Evaluation Form:
JSON output (a JSON list only):
""",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
You will be provided with a problem statement, a code snippet that supposedly addresses the problem, and a catalog of code inconsistencies.

Evaluation Steps:
1. Read the problem statement carefully to identify the functionalities required for the implementation.
2. Read the code snippet and compare it to the problem statement. Check if the code snippet covers the required functionalities.
3. Output your answer in a JSON format list.
    a) If the code snippet is correct, output: [{"inconsistency": "None", "severity": "Negligible"}].
    b) If the code snippet is incorrect, output the identified inconsistencies and their severity according to the catalog of code inconsistencies. For example: [{"inconsistency": "<inconsistency1>", "severity": "<severity1>"}, {"inconsistency": "<inconsistency2>", "severity": "<severity2>"}, ...]

Problem:
{{PROBLEM}}

Code Snippet:
{{CODE1}}

Catalog of Code Inconsistencies:
1. Missing dependency declarations that are used in the program: Negligible
2. No exception handling for unexpected events, such as invalid inputs: Negligible
3. Including inefficient or unnecessary statements: Negligible
4. Failing to handle corner cases: Small
5. Logical errors leading to incorrect outputs: Major
6. Syntax errors or compilation errors: Fatal
7. Logic not implemented, only placeholders present: Fatal
8. Timeout errors or continuous program execution without termination: Fatal
9. Referencing undefined variables or functions: Fatal
10. Other mistakes: Small

Evaluation Form:
JSON output (a JSON list only):
""",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
You will be provided with a problem statement, a code snippet that supposedly addresses the problem, a reference solution, and a catalog of code inconsistencies.
 
Evaluation Steps:
1. Read the problem statement and reference solution carefully and identify the required functionalities for the implementation. The reference solution is used to help you understand the problem, do not directly compare the code snippet to the reference code.
2. Read the code snippet and compare it to the problem statement. Check if the code snippet covers the required functionalities.
3. Output your answer in a JSON format list.
    a) If the code snippet is correct, output: [{"inconsistency": "None", "severity": "Negligible"}].
    b) If the code snippet is incorrect, output the identified inconsistencies and their severity according to the catalog of code inconsistencies. For example: [{"inconsistency": "<inconsistency1>", "severity": "<severity1>"}, {"inconsistency": "<inconsistency2>", "severity": "<severity2>"}, ...]

Problem:
{{PROBLEM}}

Reference:
{{CODE2}}

Code Snippet:
{{CODE1}}

Catalog of Code Inconsistencies:
0. Using different methods or algorithms to solve the problem: Negligible
1. Missing dependency declarations that are used in the program: Negligible
2. No exception handling for unexpected events, such as invalid inputs: Negligible
3. Including inefficient or unnecessary statements: Negligible
4. Failing to handle corner cases: Small
5. Logical errors leading to incorrect outputs: Major
6. Syntax errors or compilation errors: Fatal
7. Logic not implemented, only placeholders present: Fatal
8. Timeout errors or continuous program execution without termination: Fatal
9. Referencing undefined variables or functions: Fatal
10. Other mistakes: Small

Evaluation Form:
JSON output (a JSON list only):`
""",
        }
    ]
]


dual_step_prompt = {
    "compare_prompt": [
        [
            {
                "role": "system",
                "content": """\
You will be provided with an algorithm contest problem. This problem will contain four parts: the problem statement, input description, output description, and several input-output pair examples.
Then, you will be provided with a code snippet that supposedly addresses the problem in Python.
Your task is to check if the code snippet covers the required functionalities. Only output the evaluation, do not provide a corrected version.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
{{PROBLEM}}
\"\"\"
Code Snippet: \"\"\"python
{{CODE1}}
\"\"\"

There are also constraints on the input range  (e.g. 1 <= n <= 10^6), and programs running longer than 10 seconds will be treated as having timeout errors. Therefore, the correct code snippet needs to have both the correct logic and time complexity.
Read the code snippet carefully and analyze it. Check if the code snippet covers all the required functionalities of the problem.
"""
            },
            {
                "role": "assistant",
                "content": """\
Evaluation:
"""
            }
        ],
        [
            {
                "role": "system",
                "content": """\
You will be provided with an algorithm contest problem. This problem will contain four parts: the problem statement, input description, output description, and several input-output pair examples.
Then, you will be provided with a code snippet that supposedly addresses the problem in Python, and a reference answer.
Your task is to check if the code snippet covers the required functionalities. Only output the evaluation, do not provide a corrected version.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
{{PROBLEM}}
\"\"\"
Reference Solution: \"\"\"{{LANGUAGE}}
{{CODE2}}
\"\"\"
Code Snippet: \"\"\"{{LANGUAGE}}
{{CODE1}}
\"\"\"

There are also constraints on the input range  (e.g. 1 <= n <= 10^6), and programs running longer than 10 seconds will be treated as having timeout errors. Therefore, the correct code snippet needs to have both the correct logic and appropriate time complexity. However, it's not necessary to compare the efficiency of the code snippet to the reference code.
Read the code snippet carefully and analyze it. Check if the code snippet covers all the required functionalities of the problem.
"""
            },
            {
                "role": "assistant",
                "content": """\
Evaluation:
"""
            }
        ],
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement and a code snippet that supposedly addresses the problem.
Your task is to check if the code snippet covers the required functionalities.
If the code snippet is correct, output your reason.
If the code snippet is incorrect, list the mistakes and explain the reasons.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
{{PROBLEM}}
\"\"\"
Code Snippet: \"\"\"Python
{{CODE1}}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
Evaluation:
"""
            }
        ],
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement, a code snippet that supposedly addresses the problem, and a reference solution.
The reference solution is used to help you understand the problem, do not directly compare the code snippet to the reference code.
Your task is to check if the code snippet covers the required functionalities.
If the code snippet is correct, output your reason.
If the code snippet is incorrect, list the mistakes and explain the reasons.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
{{PROBLEM}}
\"\"\"
Reference Solution: \"\"\"Python
{{CODE2}}
\"\"\"
Code Snippet: \"\"\"Python
{{CODE1}}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
Evaluation:
"""
            }
        ],
    ],
    "analyze_prompt": [
        [
            {
                "role": "system",
                "content": """\
You will be provided with an analysis result of a code snippet.
If the analysis believes that the code snippet is correct, output: "Yes". Otherwise, output: "No".
""",
            },
            {
                "role": "user",
                "content": """\
Analysis Result:\"\"\"
{{MISTAKES}}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
Final Answer (Yes or No):
"""
            }
        ],
    ],
}
