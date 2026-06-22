import numpy as np
from tts_bench.metrics.base import BaseMetric
import utmosv2

model = utmosv2.create_model(pretrained=True)

class UTMOSV2(BaseMetric):
    
    def __init__(self):
        pass
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int= 16000) -> float:
        # every metric must have this implemented
        # Transcribe audio using faster-whisper
        audio = np.reshape(audio, (1,-1,))
        
        return model.predict(data=audio, sr=int(sr)).cpu().numpy()[0]

