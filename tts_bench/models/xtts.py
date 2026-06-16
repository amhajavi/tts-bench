from tts_bench.models.base import BaseTTSModel

import torch

from TTS.api import TTS

class XTTSWrapper(BaseTTSModel):
    
    sample_rate = 24000
    
    def __init__(self, **kwargs):
        super(XTTSWrapper).__init__()
                
        self.language = kwargs.get("language", "en")

        self.tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    
    def synthesize(self, text, **kwargs):
        
        voice_sample = kwargs.get("voice_sample", None)
        
        wav = self.tts_model.tts(text=text, speaker_wav=voice_sample, language=self.language)
        
        wav = torch.tensor(wav)
        
        return wav, self.sample_rate