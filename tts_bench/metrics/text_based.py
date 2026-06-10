import numpy as np
from faster_whisper import WhisperModel
from jiwer import wer as compute_wer

class WER:
    
    def __init__(self, model_size: str = "base"):
        self.model = WhisperModel(model_size, device="cuda", compute_type="float16")
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None) -> float:
        # every metric must have this implemented
        # Transcribe audio using faster-whisper
        audio = np.reshape(audio, (-1,))
        segments, _ = self.model.transcribe(audio,  language="en")
        transcription = " ".join([segment.text for segment in segments])
        
        # Compute WER between transcription and reference text
        error_rate = compute_wer(text, transcription)
        return error_rate

