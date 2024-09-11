python ./conala/code_score.py \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 0 \
--temperature 0 \
--return_type "helpful_score" \
--num_samples 3

python ./conala/code_score.py \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 1 \
--temperature 0 \
--return_type "helpful_score" \
--num_samples 3

python ./conala/code_score.py \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 2 \
--temperature 0 \
--return_type "0_to_4_score_usefulness" \
--num_samples 3

python ./conala/code_score.py \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 3 \
--temperature 0 \
--return_type "0_to_4_score_usefulness" \
--num_samples 3

python ./conala/code_score.py \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 4 \
--temperature 0 \
--return_type "inconsistency_level" \
--num_samples 3

python ./conala/code_score.py \
--model gpt-3.5-turbo-1106 \
--step 1 \
--compare_prompt 5 \
--temperature 0 \
--return_type "inconsistency_level" \
--num_samples 3

python ./conala/code_score.py \
--model gpt-3.5-turbo-1106 \
--step 2 \
--compare_prompt 0 \
--analyze_prompt 0 \
--temperature 0 \
--return_type helpful_score \
--num_samples 3

python ./conala/code_score.py \
--model gpt-3.5-turbo-1106 \
--step 2 \
--compare_prompt 1 \
--analyze_prompt 0 \
--temperature 0 \
--return_type helpful_score \
--num_samples 3
