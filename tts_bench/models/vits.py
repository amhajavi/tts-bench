from tts_bench.models.base import BaseTTSModel
import torch

from TTS.api import TTS

class VITSWrapper(BaseTTSModel):
    
    name = "VITS"
    sample_rate = 22050
    
    def __init__(self, **kwargs):
        super(VITSWrapper).__init__()
                
        self.language = kwargs.get("language", "en")

        self.tts_model = TTS("tts_models/en/vctk/vits")
    
    def synthesize(self, text, **kwargs):
        
        vits_speaker = kwargs.get("vits-speaker", None)
        
        wav = self.tts_model.tts(text=text, speaker=vits_speaker)
        
        wav = torch.tensor(wav)
        
        return wav, self.sample_rate