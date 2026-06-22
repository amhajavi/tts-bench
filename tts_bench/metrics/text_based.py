import torch
import numpy as np

from faster_whisper import WhisperModel
from tts_bench.metrics.base import BaseMetric
from jiwer import wer as compute_wer, cer as compute_cer

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
        
        # Compute WER between transcription and reference text
        error_rate = compute_wer(text, transcription)
        return error_rate

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
        # Compute CER between transcription and reference text
        error_rate = compute_cer(text, transcription)
        return error_rate
    
    def load_to_device(self, device: str = "cuda"):
        self.model = WhisperModel('base', device=device, compute_type="float16")
    
    def unload_from_device(self):
        self.model = None
        torch.cuda.empty_cache()