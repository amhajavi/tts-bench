import torch
import utmosv2
import numpy as np

from tts_bench.metrics.base import BaseMetric


class UTMOSV2(BaseMetric):
    
    model = None
    
    def __init__(self):
        pass
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int= 16000) -> float:
        if self.model is None:
            raise ValueError("Model is not loaded. Please call load_to_device() before computing metrics.")
        # every metric must have this implemented
        # Transcribe audio using faster-whisper
        audio = np.reshape(audio, (1,-1,))
        
        return self.model.predict(data=audio, sr=int(sr), verbose=False).cpu().numpy()[0]

    def load_to_device(self, device: str = "cuda"):
        self.model = utmosv2.create_model(pretrained=True, device=device)
    
    def unload_from_device(self):
        self.model = None
        torch.cuda.empty_cache()