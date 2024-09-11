python convert_llama_weights_to_hf.py \
    --input_dir "CodeLlama-34b-Instruct" \
    --model_size "34B" \
    --output_dir "codellama/CodeLlama-34b-Instruct-hf"

python convert_llama_weights_to_hf.py \
    --input_dir "llama3/Meta-Llama-3-70B-Instruct" \
    --model_size "70B" \
    --output_dir "codellama/Meta-Llama-3-70B-Instruct-hf" \
    --llama_version 3

python convert_llama_weights_to_hf.py \
    --input_dir "llama3/Meta-Llama-3-8B-Instruct" \
    --model_size "8B" \
    --output_dir "llama3/Meta-Llama-3-8B-Instruct-hf" \
    --llama_version 3