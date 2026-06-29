import torch
import numpy as np

from tts_bench.metrics.base import BaseMetric
from torchmetrics.functional.audio.dnsmos import deep_noise_suppression_mean_opinion_score

class DNSMOS(BaseMetric):
    
    model = None
    device = None
    
    def __init__(self):
        pass
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int= 16000) -> float:
        # every metric must have this implemented
        # Transcribe audio using faster-whisper
        audio = np.reshape(audio, (1,-1,))
        
        return deep_noise_suppression_mean_opinion_score(preds=audio, fs=int(sr), personalized=False, device=self.device).cpu().numpy()[0][0]

    def load_to_device(self, device: str = "cuda"):
        self.device = device
    
    def unload_from_device(self):
        self.device = None
        torch.cuda.empty_cache()