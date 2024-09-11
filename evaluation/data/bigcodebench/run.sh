sudo docker rm eval

sudo docker run -v $(pwd):/app \
--name eval \
-e http_proxy=http://host.docker.internal:7890 \
-e https_proxy=http://host.docker.internal:7890 \
--add-host=host.docker.internal:host-gateway \
bigcodebench/bigcodebench-evaluate:latest \
--split instruct \
--subset full \
--samples sanitized_calibrated_samples/instruct/codellama--CodeLlama-13b-Instruct-hf--bigcodebench-instruct--vllm-0-1-sanitized-calibrated.jsonl \
--max-as-limit 40960 \
--max-data-limit 40960 \
--max-stack-limit 40960