template_prompt = [
    {
        "role": "system",
        "content": """\
[Information]
Problem Statement:
{{PROBLEM}}
{{EXAMPLE}}

Code Snippet:
{{CODE1}}
[System]
We would like to request your analysis of the correctness of a code snippet. Please consider only the correctness of the code snippet, not its efficiency or style. Your job is only to determine whether the code snippet is correct or not, do not try to fix the code.
There are a few other referees assigned to the same task. Your responsibility is to discuss with them and think critically before making your final judgment. Feel free to ask them questions or provide your thoughts on their analysis.
{{HISTORY}}

{{ROLE}}
Now it's your time to talk, {{NAME}}!
""",
    }
]

final_prompt = [
    {
        "role": "system",
        "content": """\
[System]
We need your feedback on the correctness of a code snippet.
Several other referees have reviewed the code, and your task is to summarize their discussions.
Below is the history of their conversations:
{{HISTORY}}
Please provide your final judgment in a "Yes" or "No" format.
""",
    },
    {
        "role": "assistant",
        "content": """\
Final Judgement (Yes/No):
""",
    },
]
