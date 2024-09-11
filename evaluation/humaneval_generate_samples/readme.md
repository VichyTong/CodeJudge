1. Generate code samples with Code Llama - Instruct 13B
```bash
bash run.sh
```

2. Extract samples from .jsonl.gz files and combine them into one file
```
bash extract.sh
bash combine.sh
```

3. Generate code result using Dockerfile following tutorials at the [official implementation](https://github.com/THUDM/CodeGeeX/blob/main/codegeex/benchmark/README.md).
```bash
docker pull rishubi/codegeex:latest
sudo docker run -it --gpus all --mount type=bind,source="<YOUR_PATH/evaluation/generate_samples/data>",target="/data" rishubi/codegeex
```
In the docker container, you should first uncomment the warning lines in `/workspace/CodeGeeX/codegeex/benchmark/execution.py`, then run the test shell:
```bash
cd /workspace/CodeGeeX
bash scripts/evaluate_humaneval_x.sh <RESULT_FILE> <LANG> <N_WORKERS>
```
Example:
```bash
bash scripts/evaluate_humaneval_x.sh /data/cpp_inspect.jsonl cpp 32
bash scripts/evaluate_humaneval_x.sh /data/java_inspect.jsonl java 32
bash scripts/evaluate_humaneval_x.sh /data/js_inspect.jsonl js 32
bash scripts/evaluate_humaneval_x.sh /data/python_inspect.jsonl python 32
bash scripts/evaluate_humaneval_x.sh /data/go_inspect.jsonl go 32
bash scripts/evaluate_humaneval_x.sh /data/cpp_test.jsonl cpp 32
bash scripts/evaluate_humaneval_x.sh /data/java_test.jsonl java 32
bash scripts/evaluate_humaneval_x.sh /data/js_test.jsonl js 32
bash scripts/evaluate_humaneval_x.sh /data/python_test.jsonl python 32
bash scripts/evaluate_humaneval_x.sh /data/go_test.jsonl go 32
```

4. Sum all data to `evaluation/data/humaneval/test_cases`

```bash
python get_dataset.py
```