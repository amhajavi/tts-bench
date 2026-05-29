import torch

import numpy as np

class BaseTTSModel:
    
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    def synthesize(self, text: str) -> np.ndarray:
        # every model adapted must implement this
        raise NotImplementedError