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
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement and a code snippet that supposedly addresses the problem in {{LANGUAGE}}.
Your task is to check if the code snippet covers the required functionalities. Think step by step.
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
Your task is to check if the code snippet covers the required functionalities. Think step by step.
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
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement and a code snippet that supposedly addresses the problem in {{LANGUAGE}}.
Your task is to check if the code snippet covers the required functionalities. Think step by step.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
You are given an array arr of integers and you need to return sum of magnitudes of integers multiplied by product of all signs of each number in the array, represented by 1, -1 or 0. Note: return None for empty arr.
>>> prod_signs([1, 2, 2, -4]) == -9
>>> prod_signs([0, 1]) == 0
>>> prod_signs([]) == None

\"\"\"
Reference Solution: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        if (arr.contains(0)) {
            return Optional.of(0);
        }
        int prod = (int) (-2 * (arr.stream().filter(p -> p < 0).count() % 2) + 1);
        return Optional.of(prod * (arr.stream().map(Math::abs).reduce(Integer::sum)).get());
    }
}
\"\"\"
Code Snippet: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        int product = 1;
        int sum = 0;
        for (int i = 0; i < arr.size(); i++) {
            int num = arr.get(i);
            if (num < 0) {
                product *= -1;
            } else if (num > 0) {
                product *= 1;
            }
            sum += Math.abs(num);
        }
        return Optional.of(product * sum);
    }
}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
1. The problem statement requires a function that takes an array of integers and returns the sum of the absolute values of the integers, multiplied by the product of their signs. If the array is empty, the function should return None. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. 
2. The provided code snippet starts by checking if the array is empty and returns None if it is, which is correct according to the problem statement. It then initializes a product variable to 1 and a sum variable to 0. It iterates over the array, and for each number, it multiplies the product by -1 if the number is negative, and by 1 if the number is positive. It also adds the absolute value of the number to the sum. Finally, it returns the product multiplied by the sum. 
3. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. However, the code snippet does not handle this case correctly. In conclusion, the code snippet does not fully cover the required functionalities of the problem statement because it does not handle the case where the array contains a zero correctly.
"""
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
Your task is to check if the code snippet covers the required functionalities. Think step by step.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
You are given an array arr of integers and you need to return sum of magnitudes of integers multiplied by product of all signs of each number in the array, represented by 1, -1 or 0. Note: return None for empty arr.
>>> prod_signs([1, 2, 2, -4]) == -9
>>> prod_signs([0, 1]) == 0
>>> prod_signs([]) == None

\"\"\"
Reference Solution: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        if (arr.contains(0)) {
            return Optional.of(0);
        }
        int prod = (int) (-2 * (arr.stream().filter(p -> p < 0).count() % 2) + 1);
        return Optional.of(prod * (arr.stream().map(Math::abs).reduce(Integer::sum)).get());
    }
}
\"\"\"
Code Snippet: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        int product = 1;
        int sum = 0;
        for (int i = 0; i < arr.size(); i++) {
            int num = arr.get(i);
            if (num < 0) {
                product *= -1;
            } else if (num > 0) {
                product *= 1;
            }
            sum += Math.abs(num);
        }
        return Optional.of(product * sum);
    }
}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
1. The problem statement requires a function that takes an array of integers and returns the sum of the absolute values of the integers, multiplied by the product of their signs. If the array is empty, the function should return None. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. 
2. The provided code snippet starts by checking if the array is empty and returns None if it is, which is correct according to the problem statement. It then initializes a product variable to 1 and a sum variable to 0. It iterates over the array, and for each number, it multiplies the product by -1 if the number is negative, and by 1 if the number is positive. It also adds the absolute value of the number to the sum. Finally, it returns the product multiplied by the sum. 
3. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. However, the code snippet does not handle this case correctly. In conclusion, the code snippet does not fully cover the required functionalities of the problem statement because it does not handle the case where the array contains a zero correctly.
"""
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
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement and a code snippet that supposedly addresses the problem in {{LANGUAGE}}.
Your task is to check if the code snippet covers the required functionalities. Do not provide a corrected version.
Evaluation Steps:
1. Read the problem statement carefully and identify the required functionalities of the implementation. You can refer to the example and reference answer to understand the problem better.
2. Read the code snippet and analyze its logic. Check if the code snippet covers all the required functionalities of the problem.
3. Finally, conclude your evaluation.
Think step by step.
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
Think step by step.
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
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement and a code snippet that supposedly addresses the problem in {{LANGUAGE}}.
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
You are given an array arr of integers and you need to return sum of magnitudes of integers multiplied by product of all signs of each number in the array, represented by 1, -1 or 0. Note: return None for empty arr.
>>> prod_signs([1, 2, 2, -4]) == -9
>>> prod_signs([0, 1]) == 0
>>> prod_signs([]) == None

\"\"\"
Reference Solution: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        if (arr.contains(0)) {
            return Optional.of(0);
        }
        int prod = (int) (-2 * (arr.stream().filter(p -> p < 0).count() % 2) + 1);
        return Optional.of(prod * (arr.stream().map(Math::abs).reduce(Integer::sum)).get());
    }
}
\"\"\"
Code Snippet: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        int product = 1;
        int sum = 0;
        for (int i = 0; i < arr.size(); i++) {
            int num = arr.get(i);
            if (num < 0) {
                product *= -1;
            } else if (num > 0) {
                product *= 1;
            }
            sum += Math.abs(num);
        }
        return Optional.of(product * sum);
    }
}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
1. The problem statement requires a function that takes an array of integers and returns the sum of the absolute values of the integers, multiplied by the product of their signs. If the array is empty, the function should return None. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. 
2. The provided code snippet starts by checking if the array is empty and returns None if it is, which is correct according to the problem statement. It then initializes a product variable to 1 and a sum variable to 0. It iterates over the array, and for each number, it multiplies the product by -1 if the number is negative, and by 1 if the number is positive. It also adds the absolute value of the number to the sum. Finally, it returns the product multiplied by the sum. 
3. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. However, the code snippet does not handle this case correctly. In conclusion, the code snippet does not fully cover the required functionalities of the problem statement because it does not handle the case where the array contains a zero correctly.
"""
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
You are given an array arr of integers and you need to return sum of magnitudes of integers multiplied by product of all signs of each number in the array, represented by 1, -1 or 0. Note: return None for empty arr.
>>> prod_signs([1, 2, 2, -4]) == -9
>>> prod_signs([0, 1]) == 0
>>> prod_signs([]) == None

\"\"\"
Reference Solution: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        if (arr.contains(0)) {
            return Optional.of(0);
        }
        int prod = (int) (-2 * (arr.stream().filter(p -> p < 0).count() % 2) + 1);
        return Optional.of(prod * (arr.stream().map(Math::abs).reduce(Integer::sum)).get());
    }
}
\"\"\"
Code Snippet: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        int product = 1;
        int sum = 0;
        for (int i = 0; i < arr.size(); i++) {
            int num = arr.get(i);
            if (num < 0) {
                product *= -1;
            } else if (num > 0) {
                product *= 1;
            }
            sum += Math.abs(num);
        }
        return Optional.of(product * sum);
    }
}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
1. The problem statement requires a function that takes an array of integers and returns the sum of the absolute values of the integers, multiplied by the product of their signs. If the array is empty, the function should return None. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. 
2. The provided code snippet starts by checking if the array is empty and returns None if it is, which is correct according to the problem statement. It then initializes a product variable to 1 and a sum variable to 0. It iterates over the array, and for each number, it multiplies the product by -1 if the number is negative, and by 1 if the number is positive. It also adds the absolute value of the number to the sum. Finally, it returns the product multiplied by the sum. 
3. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. However, the code snippet does not handle this case correctly. In conclusion, the code snippet does not fully cover the required functionalities of the problem statement because it does not handle the case where the array contains a zero correctly.
"""
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
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement and a code snippet that supposedly addresses the problem in {{LANGUAGE}}.
Your task is to check if the code snippet covers the required functionalities. Do not provide a corrected version.
Evaluation Steps:
1. Read the problem statement carefully and identify the required functionalities of the implementation. You can refer to the example and reference answer to understand the problem better.
2. Read the code snippet and analyze its logic. Check if the code snippet covers all the required functionalities of the problem.
3. Finally, conclude your evaluation.
Think step by step.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
You are given an array arr of integers and you need to return sum of magnitudes of integers multiplied by product of all signs of each number in the array, represented by 1, -1 or 0. Note: return None for empty arr.
>>> prod_signs([1, 2, 2, -4]) == -9
>>> prod_signs([0, 1]) == 0
>>> prod_signs([]) == None

\"\"\"
Reference Solution: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        if (arr.contains(0)) {
            return Optional.of(0);
        }
        int prod = (int) (-2 * (arr.stream().filter(p -> p < 0).count() % 2) + 1);
        return Optional.of(prod * (arr.stream().map(Math::abs).reduce(Integer::sum)).get());
    }
}
\"\"\"
Code Snippet: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        int product = 1;
        int sum = 0;
        for (int i = 0; i < arr.size(); i++) {
            int num = arr.get(i);
            if (num < 0) {
                product *= -1;
            } else if (num > 0) {
                product *= 1;
            }
            sum += Math.abs(num);
        }
        return Optional.of(product * sum);
    }
}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
1. The problem statement requires a function that takes an array of integers and returns the sum of the absolute values of the integers, multiplied by the product of their signs. If the array is empty, the function should return None. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. 
2. The provided code snippet starts by checking if the array is empty and returns None if it is, which is correct according to the problem statement. It then initializes a product variable to 1 and a sum variable to 0. It iterates over the array, and for each number, it multiplies the product by -1 if the number is negative, and by 1 if the number is positive. It also adds the absolute value of the number to the sum. Finally, it returns the product multiplied by the sum. 
3. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. However, the code snippet does not handle this case correctly. In conclusion, the code snippet does not fully cover the required functionalities of the problem statement because it does not handle the case where the array contains a zero correctly.
"""
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
Think step by step.
""",
            },
            {
                "role": "user",
                "content": """\
Problem Statement: \"\"\"
You are given an array arr of integers and you need to return sum of magnitudes of integers multiplied by product of all signs of each number in the array, represented by 1, -1 or 0. Note: return None for empty arr.
>>> prod_signs([1, 2, 2, -4]) == -9
>>> prod_signs([0, 1]) == 0
>>> prod_signs([]) == None

\"\"\"
Reference Solution: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        if (arr.contains(0)) {
            return Optional.of(0);
        }
        int prod = (int) (-2 * (arr.stream().filter(p -> p < 0).count() % 2) + 1);
        return Optional.of(prod * (arr.stream().map(Math::abs).reduce(Integer::sum)).get());
    }
}
\"\"\"
Code Snippet: \"\"\"java
import java.util.*;
import java.lang.*;

class Solution {
    public Optional<Integer> prodSigns(List<Integer> arr) {
        if (arr.size() == 0) {
            return Optional.empty();
        }
        int product = 1;
        int sum = 0;
        for (int i = 0; i < arr.size(); i++) {
            int num = arr.get(i);
            if (num < 0) {
                product *= -1;
            } else if (num > 0) {
                product *= 1;
            }
            sum += Math.abs(num);
        }
        return Optional.of(product * sum);
    }
}
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": """\
1. The problem statement requires a function that takes an array of integers and returns the sum of the absolute values of the integers, multiplied by the product of their signs. If the array is empty, the function should return None. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. 
2. The provided code snippet starts by checking if the array is empty and returns None if it is, which is correct according to the problem statement. It then initializes a product variable to 1 and a sum variable to 0. It iterates over the array, and for each number, it multiplies the product by -1 if the number is negative, and by 1 if the number is positive. It also adds the absolute value of the number to the sum. Finally, it returns the product multiplied by the sum. 
3. If the array contains a zero, the product of the signs should be zero, and hence the function should return zero. However, the code snippet does not handle this case correctly. In conclusion, the code snippet does not fully cover the required functionalities of the problem statement because it does not handle the case where the array contains a zero correctly.
"""
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
        [
            {
                "role": "system",
                "content": """\
You will be given a problem statement and a code snippet in {{LANGUAGE}} that is intended to solve the problem. Your task is to critically assess the code snippet to determine if it accurately implements all the required functionalities as outlined in the problem statement. Do not provide a corrected version of the code. 

Evaluation Steps:
1. Start by carefully reading the problem statement and identifying all the required functionalities for the solution. Use the provided example to gain a deeper understanding of the problem.
2. Analyze the code snippet in detail. Ensure that the logic of the code aligns with the requirements of the problem statement. Pay particular attention to whether the code correctly implements the specific logic or formula required by the problem statement.
3. Verify if the code snippet implements all the functionalities required by the problem statement. Be vigilant for missing functionalities or incorrect logic implementation. Specifically, check if the code snippet covers all possible cases or scenarios as required by the problem statement, including edge cases or special conditions.
4. Conclude your evaluation by summarizing whether the code snippet meets all the requirements of the problem statement or not, and identify any shortcomings.

Remember, the code snippet may have incorrect logic implementation, where the logic does not correctly solve the problem, or it may have missing functionalities, where it does not cover all the requirements of the problem statement. Be sure to identify and categorize these failures in your evaluation. Pay particular attention to whether the code snippet correctly handles special conditions or edge cases, and whether it correctly implements the specific logic or formula required by the problem statement.

In your evaluation, consider the logic of the code in the context of the problem statement, and consider all possible edge cases and special conditions. Provide a detailed explanation of your evaluation, which could help to identify any misunderstandings or misconceptions. If the code snippet correctly implements the problem statement, affirm this in your evaluation.

Note: Be cautious of false negatives, where correct code snippets are incorrectly evaluated as incorrect, and false positives, where incorrect code snippets are incorrectly evaluated as correct. These could occur due to misunderstanding the logic of the code or the requirements of the problem statement.
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
You will be given a problem statement and a code snippet in {{LANGUAGE}} that is intended to solve the problem. A reference solution in {{LANGUAGE}} will also be provided for your reference. Your task is to critically evaluate the code snippet to determine if it accurately and completely addresses the problem statement.

Evaluation Steps:
1. Carefully read the problem statement and identify all the required functionalities that the solution should implement. Use the example and reference answer to gain a deeper understanding of the problem. However, do not base your evaluation on the similarity between the code snippet and the reference solution.
2. Thoroughly analyze the logic of the code snippet. Ensure that it not only addresses all the required functionalities but also implements them correctly. Pay special attention to edge cases and overlapping scenarios, if any. The code should be able to handle all possible inputs and scenarios as per the problem statement.
3. Conclude your evaluation by stating whether the code snippet fully and correctly solves the problem as per the problem statement. 

Remember, your evaluation should be based on whether the code snippet meets all the requirements of the problem statement and implements the correct logic. Do not provide a corrected version of the code snippet. Your focus should be on identifying any errors or missing functionalities in the code snippet, not on fixing them.

To avoid incorrect evaluations, consider the following:
- For positive evaluations, ensure that the code snippet not only meets the requirements of the problem statement but also implements the correct logic. Do not assume that the code is correct just because it appears to solve the problem. Make sure to consider all possible edge cases and scenarios.
- For negative evaluations, ensure that the code snippet does not meet the requirements of the problem statement or implements incorrect logic. Do not assume that the code is incorrect just because it appears different from the reference solution. Make sure to understand the logic of the code snippet and the requirements of the problem statement before making your evaluation.
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
        [
            {
                "role": "system",
                "content": """\
You will be given a problem statement and a code snippet in {{LANGUAGE}} that is intended to solve the problem. Your task is to critically evaluate the code snippet to determine if it accurately implements all the required functionalities as specified in the problem statement. Please refrain from providing a corrected version of the code.

Evaluation Steps:
1. Start by carefully reading the problem statement. Identify the key functionalities that the code needs to implement. You may refer to the provided example for a deeper understanding of the problem.
2. Scrutinize the code snippet, focusing on its logic, the programming constructs used, and the order of operations.
3. Determine whether the code snippet accurately implements all the required functionalities. Check for both obvious and subtle errors or omissions in the code.
4. Provide a comprehensive evaluation of the code snippet, explaining whether it meets the requirements of the problem statement and why.

While evaluating, pay special attention to:
1. Mathematical Operations: Ensure that mathematical operations such as addition, subtraction, modulus, etc., are implemented correctly and with the right precedence. Consider the implications of these operations in the overall functionality of the code.
2. Logical Operations: Check that logical operations like AND, OR, XOR, etc., are correctly implemented and used as required by the problem statement. Be aware of how these operations can affect the flow of the code.
3. Comparison Operations: Verify that comparison operations such as greater than, less than, equal to, etc., are correctly implemented and align with the problem statement's requirements.
4. Conditional Statements: Evaluate the correctness of conditional statements in the code. Make sure they align with the problem statement and consider their implications on the code's overall functionality.
5. Overall Functionality: Understand the overall functionality of the code in the context of the problem statement, rather than focusing only on individual operations or statements.

Remember, the goal is to accurately determine if the provided code snippet solves the problem, avoiding both false positives (incorrectly identifying a correct code snippet as incorrect) and false negatives (incorrectly identifying an incorrect code snippet as correct).
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
You will be given a problem statement and a code snippet written in {{LANGUAGE}} that attempts to solve the problem. A reference solution in {{LANGUAGE}} will also be provided. Your task is to critically evaluate the provided code snippet against the problem statement to determine if it successfully implements all the required functionalities. 

Evaluation Steps:
1. Begin by carefully reading and understanding the problem statement. Identify the key functionalities and requirements that the solution should implement. Make sure to understand any specific conditions or edge cases mentioned in the problem statement. Use the example provided and the reference solution to gain a deeper understanding of the problem.
2. Next, examine the logic of the code snippet in detail. Assess if the code snippet incorporates all the functionalities required by the problem statement. Pay special attention to how the code handles specific conditions and edge cases. Your evaluation should focus on the soundness of the code's logic and its ability to handle all possible scenarios as per the problem statement.
3. Compare the code snippet with the reference solution. Ensure they both produce the same output for the same input. This step is crucial to avoid false evaluations. The code snippet should not only generate the correct output, but also follow the correct approach as outlined in the problem statement.
4. Conclude your evaluation by stating whether the code snippet meets the problem requirements or not. 

Remember, your role is to evaluate the given code snippet, not to provide a corrected version. It's important to consider all aspects of the problem statement, including any specific requirements and edge cases, to avoid misinterpretation or overlooking any details. Your evaluation should be thorough and precise, ensuring that the code snippet either completely fulfills the problem requirements or it does not.

In order to avoid common failure cases:
- Ensure you have correctly interpreted the problem statement and its requirements before evaluating the code snippet.
- Pay close attention to the logic of the code snippet, particularly how it handles edge cases and specific requirements.
- Be critical when comparing the code snippet with the reference solution, ensuring they both follow the correct approach and produce the same output for the same input.
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
        [
            {
                "role": "system",
                "content": """\
You will be provided with a problem statement and a code snippet that supposedly addresses the problem.
Your task is to check if the code snippet covers the required functionalities.
If the code snippet is correct, output your reason.
If the code snippet is incorrect, list the mistakes and explain the reasons.

Problem:
{{PROBLEM}}

Code Snippet:
{{CODE1}}
""",
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

Problem:
{{PROBLEM}}

Reference:
{{CODE2}}

Code Snippet:
{{CODE1}}
""",
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
        [
            {
                "role": "system",
                "content": """\
You will be provided with an analysis result of a code snippet.
If the analysis believes that the code snippet is correct, output: "Yes". Otherwise, output: "No".
Please note that the analysis result may try to correct the code snippet. You should only evaluate the original code snippet.
""",
            },
            {
                "role": "user",
                "content": """\
Analysis Result: \"\"\"
The provided code snippet effectively calculates the area of a triangle by taking the length of a side and the height as inputs, using the formula 0.5 * base * height, which is the same as the reference solution's formula a * h / 2.0. Hence, the code snippet meets the required functionality.
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": "Yes"
            },
            {
                "role": "user",
                "content": """\
Analysis Result: \"\"\"
The given code snippet attempts to solve the problem by checking if the cube root of the input integer is an integer. However, this approach may not work correctly due to floating point precision issues.

The reference solution, on the other hand, takes the absolute value of the input integer and then checks if the cube of the integer part of the cube root of the absolute value is equal to the original absolute value. This approach is more reliable and covers all the required functionalities.

Therefore, the given code snippet does not cover all the required functionalities.
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": "No"
            },
            {
                "role": "user",
                "content": """\
Analysis Result: \"\"\"
The problem requires us to find the largest index of an element which is not greater than or equal to the element immediately preceding it. The reference solution iterates through the array and updates the index when it finds an element that is not greater than the element immediately preceding it.

Let's evaluate the given code snippet:

```
def can_arrange(arr):

    pass
```
The given code snippet is incomplete and does not contain any implementation.

To address the problem statement, we need to iterate through the array and compare each element with the element immediately preceding it. If we find an element that is not greater than the preceding element, we need to update the index. Finally, we return the index.

Here's the complete code snippet to address the problem:

```
def can_arrange(arr):
    ind = -1
    for i in range(1, len(arr)):
        if arr[i] < arr[i-1]:
            ind = i
    return ind
```
This code snippet iterates through the array and updates the index when it finds an element that is not greater than the element immediately preceding it. It covers the required functionalities as per the problem statement.
\"\"\"
"""
            },
            {
                "role": "assistant",
                "content": "No"
            },
            {
                "role": "user",
                "content": """\
Analysis Result: \"\"\"
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
