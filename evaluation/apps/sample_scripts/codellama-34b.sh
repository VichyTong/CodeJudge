python ./apps/code_score.py \
--test_case gpt \
--model CodeLlama-34b-Instruct \
--step 2 \
--compare_prompt 0 \
--analyze_prompt 0 \
--temperature 0.4 \
--return_type bool \
--num_samples 3

python ./apps/code_score.py \
--test_case gpt \
--model CodeLlama-34b-Instruct \
--step 2 \
--compare_prompt 1 \
--analyze_prompt 0 \
--temperature 0.4 \
--return_type bool \
--num_samples 3

python ./apps/code_score.py \
--test_case gpt \
--model CodeLlama-34b-Instruct \
--step 1 \
--compare_prompt 0 \
--temperature 0.4 \
--return_type bool \
--num_samples 3

python ./apps/code_score.py \
--test_case gpt \
--model CodeLlama-34b-Instruct \
--step 1 \
--compare_prompt 1 \
--temperature 0.4 \
--return_type bool \
--num_samples 3

python ./apps/code_score.py \
--test_case gpt \
--model CodeLlama-34b-Instruct \
--step 1 \
--compare_prompt 2 \
--temperature 0.4 \
--return_type "0_to_4_score_functional_correctness" \
--num_samples 3

python ./apps/code_score.py \
--test_case gpt \
--model CodeLlama-34b-Instruct \
--step 1 \
--compare_prompt 3 \
--temperature 0.4 \
--return_type "0_to_4_score_functional_correctness" \
--num_samples 3

python ./apps/code_score.py \
--test_case gpt \
--model CodeLlama-34b-Instruct \
--step 1 \
--compare_prompt 4 \
--temperature 0.4 \
--return_type "inconsistency_level" \
--num_samples 3

python ./apps/code_score.py \
--test_case gpt \
--model CodeLlama-34b-Instruct \
--step 1 \
--compare_prompt 5 \
--temperature 0.4 \
--return_type "inconsistency_level" \
--num_samples 3