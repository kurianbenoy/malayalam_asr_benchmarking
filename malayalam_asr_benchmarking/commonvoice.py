# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_commonvoice.ipynb.

# %% auto 0
__all__ = ['normalizer', 'load_common_voice_malayalam_dataset', 'evaluate_whisper_model_common_voice',
           'evaluate_faster_whisper_model_common_voice']

# %% ../nbs/01_commonvoice.ipynb 3
import time
from typing import List

import pandas as pd
from datasets import load_dataset, Audio
from faster_whisper import WhisperModel
from jiwer import wer, cer
from transformers import pipeline
from tqdm.notebook import tqdm
from whisper_normalizer.indic_normalizer import MalayalamNormalizer

from malayalam_asr_benchmarking.utils import (
    get_text,
    data,
    get_model_size,
    clear_gpu_memory,
    store_results_as_dataset,
)

# %% ../nbs/01_commonvoice.ipynb 5
def load_common_voice_malayalam_dataset():
    dataset = load_dataset("mozilla-foundation/common_voice_11_0", "ml", split="test")
    dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
    return dataset

# %% ../nbs/01_commonvoice.ipynb 7
normalizer = MalayalamNormalizer()

# %% ../nbs/01_commonvoice.ipynb 8
def evaluate_whisper_model_common_voice(
    model_name: str,  # The model name
    werlist: List[float],  # WER List
    cerlist: List[float],  # CER list
    modelsizelist: List[str],  # model size list
    timelist: List[float],  # time(s) list
    bs: int = 16,  # batch size. Default value is 16.
) -> None:
    """A utility function for evaluating Whisper based models in Common voice dataset malayalam subset provided a model name in huggingface.
    You can store a WER, CER, ModelSize, TimeList to calculate results cumulatively over different epochs
    """
    whisper_asr = pipeline("automatic-speech-recognition", model=model_name, device=0)
    dataset = load_common_voice_malayalam_dataset()

    predictions_raw = []
    references_raw = []
    predictions = []
    references = []

    start = time.time()
    for out in whisper_asr(data(dataset), batch_size=bs):
        predictions_raw.append(out["text"])
        references_raw.append(out["reference"][0])
        predictions.append(normalizer((out["text"])))
        references.append(normalizer(out["reference"][0]))

    end = time.time()
    print(f"Total time taken: {end - start}")
    timelist.append(end - start)
    modelsizelist.append(get_model_size(whisper_asr.model))
    rwer = wer(references, predictions)
    rwer = round(100 * rwer, 2)
    werlist.append(rwer)
    print(f"The WER of model: {rwer}")

    rcer = cer(references, predictions)
    rcer = round(100 * rcer, 2)
    cerlist.append(rcer)
    print(f"The CER of model: {rcer}")

    # common utility function to save pandas dataframe results
    # Take predictions, references, model_name, wer, cer, total_time, model_size, saving_name

    store_results_as_dataset(
        predictions,
        predictions_raw,
        references,
        references_raw,
        model_name,
        end - start,
        get_model_size(whisper_asr.model),
        rwer,
        rcer,
        "commonvoice.parquet",
    )

    clear_gpu_memory()
    del whisper_asr

# %% ../nbs/01_commonvoice.ipynb 19
def evaluate_faster_whisper_model_common_voice(
    model_name: str,  # The model name
    werlist: List[float],  # WER List
    cerlist: List[float],  # CER list
    modelsizelist: List[str],  # model size list
    timelist: List[float],  # time(s) list
    bs: int = 16,  # batch size. Default value is 16.
    compute_type: str = "float16",  # The compute type supported by faster-Whisper
    beam_size=1,  # beam size
) -> None:
    """A utility function for calculing WER in Common voice dataset provided a model name in huggingface.
    You can store a WER, CER, ModelSize, TimeList to calculate results cumulatively over different epochs
    """
    dataset = load_common_voice_malayalam_dataset()
    model = WhisperModel(model_name, device="cuda", compute_type=compute_type)

    predictions = []
    references = []
    predictions_raw = []
    references_raw = []

    start = time.time()
    for x in tqdm(dataset):
        segments, info = model.transcribe(x["audio"]["array"], beam_size=beam_size)
        predictions_raw.append(" ".join([segment.text for segment in segments]))
        references_raw.append(x["sentence"])
        predictions.append(normalizer(" ".join([segment.text for segment in segments])))
        references.append(normalizer(x["sentence"]))

    end = time.time()
    print(f"Total time taken: {end - start}")
    timelist.append(end - start)

    rwer = wer(references, predictions)
    rwer = round(100 * rwer, 2)
    werlist.append(rwer)
    print(f"The WER of model: {rwer}")

    rcer = cer(references, predictions)
    rcer = round(100 * rcer, 2)
    cerlist.append(rcer)
    print(f"The CER of model: {rcer}")

    # print(f"The model size is: {get_model_size(whisper_asr.model)}")
    # modelsizelist.append(get_model_size(whisper_asr.model))
    # df["model_size"] = get_model_size(whisper_asr.model)

    store_results_as_dataset(
        predictions,
        predictions_raw,
        references,
        references_raw,
        model_name,
        end - start,
        None,
        rwer,
        rcer,
        "commonvoice.parquet",
    )
    clear_gpu_memory()
