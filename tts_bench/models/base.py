import numpy as np

class BaseTTSModel:
    def synthesize(self, text: str) -> np.ndarray:
        # every model adapted must implement this
        raise NotImplementedError