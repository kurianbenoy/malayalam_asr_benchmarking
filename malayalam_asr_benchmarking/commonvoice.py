# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_commonvoice.ipynb.

# %% auto 0
__all__ = ['normalizer', 'load_common_voice_malayalam_dataset', 'evaluate_whisper_model_common_voice']

# %% ../nbs/01_commonvoice.ipynb 3
import time
from typing import List

import pandas as pd
from datasets import load_dataset, Audio
from jiwer import wer, cer
from transformers import pipeline
from whisper_normalizer.basic import BasicTextNormalizer

from malayalam_asr_benchmarking.utils import (
    whisper_norm,
    is_target_text_in_range,
    get_text,
    normalise,
    data,
    get_model_size,
    clear_gpu_memory,
)

# %% ../nbs/01_commonvoice.ipynb 4
def load_common_voice_malayalam_dataset():
    dataset = load_dataset("mozilla-foundation/common_voice_11_0", "ml", split="test")
    dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
    dataset = dataset.map(normalise)
    dataset = dataset.filter(is_target_text_in_range, input_columns=["norm_text"])
    return dataset

# %% ../nbs/01_commonvoice.ipynb 5
normalizer = BasicTextNormalizer()


def evaluate_whisper_model_common_voice(
    model_name: str,  # The model name
    werlist: List[float],  # WER List
    cerlist: List[float],  # CER list
    modelsizelist: List[str],  # model size list
    timelist: List[float],  # time(s) list
    bs: int = 16,  # batch size. Default value is 16.
) -> None:
    """A utility function for calculing WER in Common voice dataset provided a model name in huggingface.
    You can store a WER, CER, ModelSize, TimeList to calculate results cumulatively over different epochs
    """
    whisper_asr = pipeline("automatic-speech-recognition", model=model_name, device=0)
    dataset = load_common_voice_malayalam_dataset()

    predictions = []
    references = []

    start = time.time()
    for out in whisper_asr(data(dataset), batch_size=bs):
        predictions.append(normalizer((out["text"])))
        references.append(normalizer(out["reference"][0]))

    end = time.time()
    print(f"Total time taken: {end - start}")
    timelist.append(end - start)

    df = pd.DataFrame({"predictions": predictions, "ground_truth": references})
    df["model_name"] = model_name
    df["wer"] = df.apply(
        lambda row: wer(
            normalizer(row["ground_truth"]), normalizer(row["predictions"])
        ),
        axis=1,
    )
    df["cer"] = df.apply(
        lambda row: cer(
            normalizer(row["ground_truth"]), normalizer(row["predictions"])
        ),
        axis=1,
    )
    df["total_time"] = end - start

    rwer = wer(references, predictions)
    rwer = round(100 * rwer, 2)
    werlist.append(rwer)
    print(f"The WER of model: {rwer}")

    rcer = cer(references, predictions)
    rcer = round(100 * rcer, 2)
    cerlist.append(rcer)
    print(f"The CER of model: {rcer}")

    print(f"The model size is: {get_model_size(whisper_asr.model)}")
    modelsizelist.append(get_model_size(whisper_asr.model))
    df["model_size"] = get_model_size(whisper_asr.model)

    save_name = model_name.split("/")
    print(save_name)
    df.to_parquet(
        f"/home/commonvoice_results/{save_name[0]}_{save_name[1]}_commonvoice.parquet"
    )

    clear_gpu_memory()
