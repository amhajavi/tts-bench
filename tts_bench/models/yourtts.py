from tts_bench.models.base import BaseTTSModel

from TTS.api import TTS
import torch
class YourTTSWrapper(BaseTTSModel):
    
    sample_rate = 16000
    
    def __init__(self, **kwargs):
        super(YourTTSWrapper).__init__()
                
        self.language = kwargs.get("language", "en")
        self.tts_model = TTS("tts_models/multilingual/multi-dataset/your_tts")
    
    def synthesize(self, text, **kwargs):
        
        voice_sample = kwargs.get("voice_sample", None)
        wav = self.tts_model.tts(text=text, speaker_wav=voice_sample, language=self.language)
        wav = torch.tensor(wav)
        return wav, self.sample_rate