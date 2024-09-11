analyze_prompt = [
    {
        "role": "system",
        "content": """\
Your task is to refine the prompt given to the model to improve its performance.

Here are the original prompt instructions given to the model:
{PROMPT}

Here is a list of failure cases for the given prompt:
{FAILURE_CASES}

Note that the ground-truth are absolutely correct, the prompts may be flawed and require refinement.
Your task is to provide a concise analysis of the given prompt's performance.
The analysis should provide a summary of the common failure cases, cluster the failure cases into groups, and describe each group.
""",
    },
    {
        "role": "assistant",
        "content": """\
Analysis:
""",
    },
]

refine_prompt = [
    {
        "role": "system",
        "content": """\
You will be given an original prompt used to evaluate the correctness of a code snippet, along with an analysis of common failure cases associated with this prompt. Your task is to generate a new, improved prompt that addresses the drawbacks highlighted in the analysis.

Original prompt:
{PROMPT}

Analysis of the original prompt:
{ANALYSIS}

Please provide a concise revised prompt that resolves the issues mentioned in the analysis.
"""
    },
    {
        "role": "assistant",
        "content": """\
New Prompt:
"""
    }
]

failure_cases_prompt = """
## Case {INDEX}
Problem Statement: \"\"\"
{PROBLEM}
\"\"\"

Code Snippet: \"\"\"
{CODE1}
\"\"\"

Ground-Truth label:
{GROUND_TRUTH}

Model Evaluation:
{MODEL_OUTPUT}
"""
