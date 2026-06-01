import torch

import numpy as np

class BaseTTSModel:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    def __init__(self):
        pass
    
    def synthesize(self, text: str) -> np.ndarray:
        # every model adapted must implement this
        raise NotImplementedError