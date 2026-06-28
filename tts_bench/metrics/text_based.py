import torch
import numpy as np

from faster_whisper import WhisperModel
from tts_bench.metrics.base import BaseMetric
from jiwer import wer as compute_wer, cer as compute_cer
from tts_bench.utils.handle_money_problems import (
    strip_commas_in_numbers,
    compute_best_dollar_aware_error,
)

class WER(BaseMetric):
    
    model = None
    
    def __init__(self):
        pass
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int = 16000) -> float:
        if self.model is None:
            raise ValueError("Model is not loaded. Please call load_to_device() before computing metrics.")
        # every metric must have this implemented
        # Transcribe audio using faster-whisper
        audio = np.reshape(audio.numpy(), (-1,))
        segments, _ = self.model.transcribe(audio,  language="en")
        transcription = " ".join([segment.text for segment in segments])
        # Remove commas inside numbers from both reference and transcription
        clean_ref = strip_commas_in_numbers(text)
        clean_trans = strip_commas_in_numbers(transcription)

        # Compute WER between transcription and reference text, using dollar-aware comparisons
        error_rate = compute_best_dollar_aware_error(clean_ref, clean_trans, compute_wer)
        return error_rate

    def load_to_device(self, device: str = "cuda"):
        self.model = WhisperModel('base', device=device, compute_type="float16")
    
    def unload_from_device(self):
        self.model = None
        torch.cuda.empty_cache()

class StressPassRate(BaseMetric):
    """Returns 0.0 (pass) if WER is below the threshold, 1.0 (fail) otherwise."""

    model = None

    def __init__(self, threshold: float = 0.01):
        self.threshold = threshold

    def compute(self, audio: np.ndarray, text: str, reference: np.ndarray = None, sr: int = 16000) -> float:
        if self.model is None:
            raise ValueError("Model is not loaded. Please call load_to_device() before computing metrics.")
        audio = np.reshape(audio.numpy(), (-1,))
        segments, _ = self.model.transcribe(audio, language="en")
        transcription = " ".join([segment.text for segment in segments])
        clean_ref = strip_commas_in_numbers(text)
        clean_trans = strip_commas_in_numbers(transcription)
        error_rate = compute_best_dollar_aware_error(clean_ref, clean_trans, compute_wer)
        return 1.0 if error_rate <= self.threshold else 0.0

    def load_to_device(self, device: str = "cuda"):
        self.model = WhisperModel('base', device=device, compute_type="float16")

    def unload_from_device(self):
        self.model = None
        torch.cuda.empty_cache()

class CER(BaseMetric):
    
    model = None
    
    def __init__(self):
        pass
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int = 16000) -> float:
        if self.model is None:
            raise ValueError("Model is not loaded. Please call load_to_device() before computing metrics.")
        # Transcribe audio using faster-whisper
        audio = np.reshape(audio.numpy(), (-1,))
        segments, _ = self.model.transcribe(audio,  language="en")
        transcription = " ".join([segment.text for segment in segments])    
        # Remove commas inside numbers from both reference and transcription
        clean_ref = strip_commas_in_numbers(text)
        clean_trans = strip_commas_in_numbers(transcription)
        # Compute CER between transcription and reference text, using dollar-aware comparisons
        error_rate = compute_best_dollar_aware_error(clean_ref, clean_trans, compute_cer)
        return error_rate
    
    def load_to_device(self, device: str = "cuda"):
        self.model = WhisperModel('base', device=device, compute_type="float16")
    
    def unload_from_device(self):
        self.model = None
        torch.cuda.empty_cache()