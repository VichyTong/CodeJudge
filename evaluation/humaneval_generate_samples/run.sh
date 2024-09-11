python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang python \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 3 \
--name-override "CodeLlama_13b_Instruct_inspect"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang cpp \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 3 \
--name-override "CodeLlama_13b_Instruct_inspect"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang java \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 3 \
--name-override "CodeLlama_13b_Instruct_inspect"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang js \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 3 \
--name-override "CodeLlama_13b_Instruct_inspect"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang go \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 3 \
--name-override "CodeLlama_13b_Instruct_inspect"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang python \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 1 \
--name-override "CodeLlama_13b_Instruct_test"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang cpp \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 1 \
--name-override "CodeLlama_13b_Instruct_test"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang java \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 1 \
--name-override "CodeLlama_13b_Instruct_test"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang js \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 1 \
--name-override "CodeLlama_13b_Instruct_test"

python main.py \
--name ../model/CodeLlama-13b-Instruct-hf/ \
--lang go \
--root-dataset humaneval \
--temperature 0.2 \
--completion-limit 1 \
--name-override "CodeLlama_13b_Instruct_test"