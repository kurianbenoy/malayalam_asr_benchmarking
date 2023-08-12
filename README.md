# malayalam_asr_benchmarking

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Objective of the project

<div>

> **Note**
>
> A study to benchmark ASRs in Malayalam. Till now the project has
> benchmark based on Malayalam ASR models based in Whisper.

</div>

## Benchmarked Datasets

Till now we have mainly benchmarked on two datasets:

1.  Common Voice 11 Dataset

I have now done benchmarking on Mozilla’s [Common Voice 11 Malayalam
subset](https://huggingface.co/datasets/mozilla-foundation/common_voice_11_0/viewer/ml/train).
The benchmarking results can be found in [the below
dataset](https://huggingface.co/datasets/kurianbenoy/malayalam_common_voice_benchmarking).

2.  Malayalam Speech Corpus

I have now benchmarked on SMC’s [Malayalam Speech corpus
dataset](https://msc.smc.org.in/). The benchmarking results can be found
in [the below
dataset](https://huggingface.co/datasets/kurianbenoy/malayalam_msc_benchmarking/tree/main).

## Install

``` sh
pip install malayalam_asr_benchmarking
```

Or locally

``` sh
pip install -e .
```

## Setting up your development environment

I am developing this project with nbdev. Please take some time reading
up on nbdev … how it works,
[directives](https://nbdev.fast.ai/explanations/directives.html), etc…
by checking out [the
walk-thrus](https://nbdev.fast.ai/tutorials/tutorial.html) and
[tutorials](https://nbdev.fast.ai/tutorials/) on the [nbdev
website](https://nbdev.fast.ai/)

### Step 1: Install Quarto:

`nbdev_install_quarto`

[Other options are mentioned in getting started to
quarto](https://quarto.org/docs/get-started/)

## Step 2: Install hooks

`nbdev_install_hooks`

## Step 3: Install our library

`pip install -e '.[dev]'`

## How to use

``` python
from malayalam_asr_benchmarking.commonvoice import evaluate_whisper_model_common_voice

werlist = []
cerlist = []
modelsizelist = []
timelist = []

evaluate_whisper_model_common_voice("parambharat/whisper-tiny-ml", werlist, cerlist, modelsizelist, timelist)
```

    Downloading (…)lve/main/config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.03k/1.03k [00:00<00:00, 6.09MB/s]
    Downloading pytorch_model.bin: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 151M/151M [00:24<00:00, 6.07MB/s]
    Downloading (…)okenizer_config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 827/827 [00:00<00:00, 2.64MB/s]
    Downloading (…)olve/main/vocab.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.04M/1.04M [00:00<00:00, 1.14MB/s]
    Downloading (…)olve/main/merges.txt: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 494k/494k [00:00<00:00, 2.65MB/s]
    Downloading (…)main/normalizer.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 52.7k/52.7k [00:00<00:00, 252kB/s]
    Downloading (…)in/added_tokens.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2.11k/2.11k [00:00<00:00, 8.53MB/s]
    Downloading (…)cial_tokens_map.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2.06k/2.06k [00:00<00:00, 5.10MB/s]
    Downloading (…)rocessor_config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 185k/185k [00:02<00:00, 76.2kB/s]

    AssertionError: Torch not compiled with CUDA enabled
