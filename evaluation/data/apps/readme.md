# APPS Dataset Preprocess

1. Download the dataset (`APPS.tar.gz`) from the [APPS](https://github.com/hendrycks/apps) Github repository.

2. Use GPT-3.5-Turbo to generate programs.

```bash
export OPENAI_API_KEY=<your-API-key>
python generate_gpt_codes.py
```

3. Get the test results.

```bash
python test_one_solution.py -i 0
```

4. Get the final dataset.
```bash
python get_apps_dataset.py
```