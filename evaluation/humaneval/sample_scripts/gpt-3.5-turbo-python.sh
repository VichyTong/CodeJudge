python ./humaneval/code_score.py \
--test_case python-small-test \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 0 \
--temperature 0 \
--with_prefix \
--return_type bool \
--num_samples 1

python ./humaneval/code_score.py \
--test_case python-small-test \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 1 \
--temperature 0 \
--with_prefix \
--return_type bool \
--num_samples 1

python ./humaneval/code_score.py \
--test_case python-small-test \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 2 \
--temperature 0 \
--with_prefix \
--return_type "0_to_4_score_functional_correctness" \
--num_samples 1

python ./humaneval/code_score.py \
--test_case python-small-test \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 3 \
--temperature 0 \
--with_prefix \
--return_type "0_to_4_score_functional_correctness" \
--num_samples 1

python ./humaneval/code_score.py \
--test_case python-small-test \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 4 \
--temperature 0 \
--with_prefix \
--return_type "error_level" \
--num_samples 1

python ./humaneval/code_score.py \
--test_case python-small-test \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 5 \
--temperature 0 \
--with_prefix \
--return_type "error_level" \
--num_samples 1

python ./humaneval/code_score.py \
--test_case python-small-test \
--model gpt-3.5-turbo-1106 \
--step 2 \
--compare_prompt 0 \
--analyze_prompt 0 \
--temperature 0 \
--with_prefix \
--return_type bool \
--num_samples 1

python ./humaneval/code_score.py \
--test_case python-small-test \
--model gpt-3.5-turbo-1106 \
--step 2 \
--compare_prompt 1 \
--analyze_prompt 0 \
--temperature 0 \
--with_prefix \
--return_type bool \
--num_samples 1