python combine.py \
--directory humaneval-cpp-CodeLlama_13b_Instruct_inspect-0.2-reworded \
--language cpp \
--output_filename ./data/cpp_inspect.jsonl

python combine.py \
--directory humaneval-java-CodeLlama_13b_Instruct_inspect-0.2-reworded \
--language java \
--output_filename ./data/java_inspect.jsonl

python combine.py \
--directory humaneval-js-CodeLlama_13b_Instruct_inspect-0.2-reworded \
--language js \
--output_filename ./data/js_inspect.jsonl

python combine.py \
--directory humaneval-python-CodeLlama_13b_Instruct_inspect-0.2-reworded \
--language python \
--output_filename ./data/python_inspect.jsonl

python combine.py \
--directory humaneval-go-CodeLlama_13b_Instruct_inspect-0.2-reworded \
--language go \
--output_filename ./data/go_inspect.jsonl

python combine.py \
--directory humaneval-cpp-CodeLlama_13b_Instruct_test-0.2-reworded \
--language cpp \
--output_filename ./data/cpp_test.jsonl

python combine.py \
--directory humaneval-java-CodeLlama_13b_Instruct_test-0.2-reworded \
--language java \
--output_filename ./data/java_test.jsonl

python combine.py \
--directory humaneval-js-CodeLlama_13b_Instruct_test-0.2-reworded \
--language js \
--output_filename ./data/js_test.jsonl

python combine.py \
--directory humaneval-python-CodeLlama_13b_Instruct_test-0.2-reworded \
--language python \
--output_filename ./data/python_test.jsonl

python combine.py \
--directory humaneval-go-CodeLlama_13b_Instruct_test-0.2-reworded \
--language go \
--output_filename ./data/go_test.jsonl
