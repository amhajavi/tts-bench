import numpy as np
from tts_bench.metrics.base import BaseMetric
from faster_whisper import WhisperModel
from jiwer import wer as compute_wer, cer as compute_cer

model = WhisperModel('base', device="cuda", compute_type="float16")

class WER(BaseMetric):
    
    def __init__(self):
        pass
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int = 16000) -> float:
        # every metric must have this implemented
        # Transcribe audio using faster-whisper
        audio = np.reshape(audio.numpy(), (-1,))
        segments, _ = model.transcribe(audio,  language="en")
        transcription = " ".join([segment.text for segment in segments])
        
        # Compute WER between transcription and reference text
        error_rate = compute_wer(text, transcription)
        return error_rate

class CER(BaseMetric):
    
    def __init__(self):
        pass
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int = 16000) -> float:
        # Transcribe audio using faster-whisper
        audio = np.reshape(audio.numpy(), (-1,))
        segments, _ = model.transcribe(audio,  language="en")
        transcription = " ".join([segment.text for segment in segments])    
        # Compute CER between transcription and reference text
        error_rate = compute_cer(text, transcription)
        return error_rate