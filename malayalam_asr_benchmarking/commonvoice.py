# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_commonvoice.ipynb.

# %% auto 0
__all__ = []

# %% ../nbs/01_commonvoice.ipynb 3
import time

from datasets import load_dataset, Audio
from jiwer import wer, cer
from transformers import pipeline

from .utils import *
