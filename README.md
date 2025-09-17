<p align="center">
    <img src="paper/images/icon.png" width="150" style="margin-bottom: 0.2;"/>
<p>
<h2 align="center"> CodeJudge: Evaluating Code Generation with Large Language Models</h2>
<h5 align="center"> If you like our project, please give us a star ⭐ on GitHub for the latest update.  </h2>

## 😮 Highlights
CodeJudge is a code evaluation framework that leverages LLMs to evaluate the semantic correctness of generated code *without the need of test cases*. 

### 💡 Simple insight but efficient
Results show that CodeJudge significantly outperformed existing methods across the four LLMs we tested. Furthermore, compared to a SOTA GPT-3.5-based code evaluation method, CodeJudge achieved better results even when using a much smaller model, Llama-3-8B-Instruct.

### ⚡ Off-the-shelf framework that is easy to use
CodeJudge is an off-the-shelf evaluation framework that can be easily integrated into new LLM-based code generation systems.

## 🛠️ Requirements and Installation

* Python >= 3.10
* Pytorch >= 2.2.0
* CUDA Version >= 11.7
* Install required packages:
```bash
git clone https://github.com/VichyTong/CodeJudge
cd CodeJudge
conda create -n codejudge python=3.10 -y
conda activate codejudge
pip install -r requirements.txt
```

## 💾 Dataset Preparation
We uploaded datasets we used to test CodeJudge at [evaluation/data](evaluation/data). If you want to generate code samples by your self on HumanEval-X dataset, please follow the instruction in the [markdown file](evaluation/humaneval_generate_samples/readme.md).

## 🔽 Model Preparation

### OpenAI models
```bash
export OPENAI_API_KEY=<YOUR_API_KEY>
```

### Meta Models

1. Please follow the instructions at the [official website](https://llama.meta.com/llama-downloads/) of Code Llama and LLama-3 to get download URLs.

2. Download the model
For Code Llama:
```bash
cd evaluation/model/codellama
bash download.sh
```
For Llama-3:
```bash
cd evaluation/model/llama3
bash download.sh
```

3. Convert the model to Huggingface 🤗 format:
```bash
cd evaluation/model
bash convert.sh
```

## 🚀 Run CodeJudge
Please refer to sample scripts under sample_scripts folder for every dataset ([HumanEval-X](evaluation/humaneval/sample_scripts/), [CoNaLa](evaluation/conala/sample_scripts/), [APPS](evaluation/apps/sample_scripts/), [BigCodeBench](evaluation/bigcodebench/sample_scripts/)).

You can choose models from: `gpt-3.5-turbo-1106`, `CodeLlama-34b-Instruct`, `Meta-Llama-3-8B-Instruct`, and `Meta-Llama-3-70B-Instruct`.

For exmaple, you can run HumanEval-X test by:
```bash
cd evaluation
bash humaneval/sample_script/gpt-3.5-turbo-python.sh
```

You can also download our test results [here](https://drive.google.com/file/d/1uo4tBx6YDJjQmSUNOpgzZrdfv7lB7vxv/view?usp=sharing).

## 👍 Acknowledgement

We thank these greate works:
- [HumanEval](https://github.com/openai/human-eval) is a widely used Python dataset to evaluate code generation. 
- [HumanEval-X](https://github.com/THUDM/CodeGeeX/tree/main/codegeex/benchmark/humaneval-x) is a multi-language extension of HumanEval, including C++, Python, Java, JavaScript, Go, and Rust.
- [CoNaLa](https://conala-corpus.github.io/) is a Python code generation benchmark with 472 tasks collected from StackOverflow.
- We especially thank Dr. Evtikhiev of JetBrains Research for generously sharing the human-labeled data of the CoNaLa dataset.
- [APPS](https://github.com/hendrycks/apps) is a Python code generation benchmark that includes introductory, interview-level, and competition-level tasks collected from coding competition websites.
- [BigCodeBench](https://github.com/bigcode-project/bigcodebench) is a recently released code generation benchmark with 1,140 practical and challenging programming tasks.
- We also thank [MuliPL-E](https://github.com/nuprl/MultiPL-E) for their excellent code for sampling programs using code generation LLMs.

## Citation
If you find our work helpful, please consider citing our paper:
```
@inproceedings{tong-zhang-2024-codejudge,
    title = "{C}ode{J}udge: Evaluating Code Generation with Large Language Models",
    author = "Tong, Weixi  and  Zhang, Tianyi",
    editor = "Al-Onaizan, Yaser  and  Bansal, Mohit  and  Chen, Yun-Nung",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-main.1118",
    pages = "20032--20051"
}
```