import numpy as np

class BaseMetric:
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int = 16000) -> float:
        # every metric must have this implemented
        raise NotImplementedError
    