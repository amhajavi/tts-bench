import numpy as np

class BaseMetric:
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int = 16000) -> float:
        # every metric must have this implemented
        raise NotImplementedError
    
    def load_to_device(self, device: str = "cuda"):
        # every metric must have this implemented
        raise NotImplementedError
    
    def unload_from_device(self):
        # every metric must have this implemented
        raise NotImplementedError