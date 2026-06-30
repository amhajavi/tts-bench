import torch

import numpy as np

class BaseTTSModel:
    
    name = "BaseTTSModel"
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tts_model = None
    
    def __init__(self):
        pass
    
    def synthesize(self, text: str) -> np.ndarray:
        # every model adapted must implement this
        raise NotImplementedError
    
    def load_to_device(self):
        if self.tts_model is not None:
            self.tts_model.to(self.device)
            
    def unload_from_device(self):
        if self.tts_model is not None:
            self.tts_model.cpu()
    