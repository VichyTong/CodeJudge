single_step_prompt = [
    [
        {
            "role": "system",
            "content": """\
Determine the helpfulness of the code snippet. Output a score from 0 to 4 where 0 means the code snippet is not helpful at all and 4 means the code snippet is very helpful.

Problem:
{{PROBLEM}}

Code Snippet:
{{CODE1}}
""",
        },
        {
            "role": "assistant",
            "content": "Helpfulness (0-4): ",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
Determine the helpfulness of the code snippet. Output a score from 0 to 4 where 0 means the code snippet is not helpful at all and 4 means the code snippet is very helpful.

Problem:
{{PROBLEM}}

Reference Code:
{{CODE2}}

Code Snippet:
{{CODE1}}
""",
        },
        {
            "role": "assistant",
            "content": "Helpfulness (0-4): ",
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
Usefulness (0-4) Usefulness of the code snippet based on the problem description.

- A score of 0: Snippet is not at all helpful, it is irrelevant to the problem.
- A score of 1: Snippet is slightly helpful, it contains information relevant to the problem, but it is easier to write the solution from scratch.
- A score of 2: Snippet is somewhat helpful, it requires significant changes (compared to the size of the snippet), but is still useful.
- A score of 3: Snippet is helpful, but needs to be slightly changed to solve the problem.
- A score of 4: Snippet is very helpful, it solves the problem.

Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the problem. Check if the code snippet covers all required functionalities of the problem, and if it presents them in a clear and logical order. 
3. Assign a score for usefulness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{PROBLEM}}

Code Snippet:

{{CODE1}}

Evaluation Form:
Usefulness (scores ONLY)
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
Usefulness (0-4) Usefulness of the code snippet based on the problem description and the comparison of reference code.

- A score of 0: Snippet is not at all helpful, it is irrelevant to the problem.
- A score of 1: Snippet is slightly helpful, it contains information relevant to the problem, but it is easier to write the solution from scratch.
- A score of 2: Snippet is somewhat helpful, it requires significant changes (compared to the size of the snippet), but is still useful.
- A score of 3: Snippet is helpful, but needs to be slightly changed to solve the problem.
- A score of 4: Snippet is very helpful, it solves the problem.

Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the problem and reference code. Check if the code snippet covers all required functionalities of the problem, and if it presents them in a clear and logical order. 
3. Assign a score for usefulness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{PROBLEM}}

Reference Code:

{{CODE2}}

Code Snippet:

{{CODE1}}

Evaluation Form:
Usefulness (scores ONLY)
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
You will be provided with a problem statement, a single-line Python code snippet that supposedly addresses the problem, and a catalog of code inconsistencies.

Evaluation Steps:
1. Read the problem statement and the code snippet to check if the code snippet covers the required functionalities.
2. Output your answer in a JSON format list.
    a) If the code snippet covers the required functionalities, output: [{"inconsistency": "None", "severity": "Negligible"}].
    b) If the code snippet does not cover the required functionalities, output the identified inconsistencies and their severity according to the catalog of code inconsistencies.
    For example: [{"inconsistency": "<inconsistency1>", "severity": "<severity1>"}, {"inconsistency": "<inconsistency2>", "severity": "<severity2>"}, ...]

Problem statement:
{{PROBLEM}}

Code Snippet:
```
{{CODE1}}
```

Catalog of Code Inconsistencies:
1. Missing dependency declarations that are used in the program: Negligible
2. No exception handling for unexpected events, such as invalid inputs: Negligible
3. Including inefficient or unnecessary statements: Negligible
4. Failing to handle corner cases: Small
5. Logical errors leading to incorrect outputs: Major
6. Missing important implementations of functionalities: Fatal
7. Syntax errors or compilation errors: Fatal
8. Out of bound errors when accessing an array or list: Fatal
9. Timeout errors or continuous program execution without termination: Fatal
10. Referencing undefined variables or functions: Fatal
11. Other mistakes: Small
""",
        }
    ],
    [
        {
            "role": "system",
            "content": """\
You will be provided with a problem statement, a single-line Python code snippet that supposedly addresses the problem, a reference solution, and a catalog of code inconsistencies.
 
Evaluation Steps:
1. Read the problem statement and the code snippet to check if the code snippet covers the required functionalities.
2. Output your answer in a JSON format list.
    a) If the code snippet covers the required functionalities, output: [{"inconsistency": "None", "severity": "Negligible"}].
    b) If the code snippet does not cover the required functionalities, output the identified inconsistencies and their severity according to the catalog of code inconsistencies.
    For example: [{"inconsistency": "<inconsistency1>", "severity": "<severity1>"}, {"inconsistency": "<inconsistency2>", "severity": "<severity2>"}, ...]

Problem statement:
{{PROBLEM}}

Reference solution:
```
{{CODE2}}
```

Code Snippet:
```
{{CODE1}}
```

Catalog of Code Inconsistencies:
0. Using different methods or algorithms to solve the problem: Negligible
1. Missing dependency declarations that are used in the program: Negligible
2. No exception handling for unexpected events, such as invalid inputs: Negligible
3. Including inefficient or unnecessary statements: Negligible
4. Failing to handle corner cases: Small
5. Logical errors leading to incorrect outputs: Major
6. Missing important implementations of functionalities: Fatal
7. Syntax errors or compilation errors: Fatal
8. Out of bound errors when accessing an array or list: Fatal
9. Timeout errors or continuous program execution without termination: Fatal
10. Referencing undefined variables or functions: Fatal
11. Other mistakes: Small
""",
        }
    ],
]

dual_step_prompt = {
    "compare_prompt": [
        [
            {
                "role": "system",
                "content": """\
You will be provided with a Python problem statement and a short code snippet that supposedly addresses the problem.

First assign a score of helpfulness to the code snippet. This score should be between 0 and 100, where 0 means that the code snippet is totally not helpful, and 100 means that the code snippet is very helpful and solves the problem.
If the code snippet is totally not helpful and is irrelevant to the problem, output your reason.
If the code snippet is slightly helpful and contains information relevant to the problem, output the relevant information.
If the code snippet is somewhat helpful and requires significant changes (compared to the size of the snippet), output the significant changes needed.
If the code snippet is helpful but needs to be slightly changed to solve the problem, output the slight changes needed.
If the code snippet is very helpful and solves the problem, output your reason.

Problem:
{{PROBLEM}}

Code Snippet:
{{CODE1}}

Evaluation Form:
Score:
""",
            }
        ],
        [
            {
                "role": "system",
                "content": """\
You will be provided with a Python problem statement, a short code snippet that supposedly addresses the problem, and a reference solution.
The reference solution is used to help you understand the problem, do not directly compare the code snippet to the reference code. The reference answer is not the only helpful way to solve the problem.

First assign a score of helpfulness to the code snippet. This score should be between 0 and 100, where 0 means that the code snippet is totally not helpful, and 100 means that the code snippet is very helpful and solves the problem.
If the code snippet is totally not helpful and is irrelevant to the problem, output your reason.
If the code snippet is slightly helpful and contains information relevant to the problem, output the relevant information.
If the code snippet is somewhat helpful and requires significant changes (compared to the size of the snippet), output the significant changes needed.
If the code snippet is helpful but needs to be slightly changed to solve the problem, output the slight changes needed.
If the code snippet is very helpful and solves the problem, output your reason.

Problem:
{{PROBLEM}}

Reference:
{{CODE2}}

Code Snippet:
{{CODE1}}

Evaluation Form:
Score:
""",
            }
        ],
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement and a code snippet that supposedly addresses the problem in {{LANGUAGE}}.
Your task is to check if the code snippet covers the required functionalities. Do not provide a corrected version.
Evaluation Steps:
1. Read the problem statement carefully and identify the required functionalities of the implementation. You can refer to the example to understand the problem better.
2. Read the code snippet and analyze its logic. Check if the code snippet covers all the required functionalities of the problem.
3. Finally, conclude your evaluation.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
{{PROBLEM}}
{{EXAMPLE}}
\"\"\"
Code Snippet: \"\"\"{{LANGUAGE}}
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
You will be provided with a problem statement, a code snippet that supposedly addresses the problem in {{LANGUAGE}}, and a reference solution in {{LANGUAGE}}.
Your task is to check if the code snippet covers the required functionalities. Do not provide a corrected version.
Evaluation Steps:
1. Read the problem statement carefully and identify the required functionalities of the implementation. You can refer to the example and reference answer to understand the problem better.
2. Read the code snippet and analyze its logic. Check if the code snippet covers all the required functionalities of the problem.
3. Finally, conclude your evaluation.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
{{PROBLEM}}
{{EXAMPLE}}
\"\"\"
Reference Solution: \"\"\"{{LANGUAGE}}
{{CODE2}}
\"\"\"
Code Snippet: \"\"\"{{LANGUAGE}}
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
What score does the analysis result indicate?
Output the score only.

Analysis Result:
{{MISTAKES}}
""",
            },
            {
                "role": "assistant",
                "content": "Score (0-100):",
            },
        ],
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
