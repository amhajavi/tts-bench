from tts_bench.models.base import BaseTTSModel

from TTS.api import TTS

class YourTTSWrapper(BaseTTSModel):
    
    sample_rate = 16000
    
    def __init__(self):
        super(YourTTSWrapper).__init__()
                
        self.tts_model = TTS("tts_models/multilingual/multi-dataset/your_tts")
    
    def synthesize(self, text, voice_sample=None, language="en", **kwargs):
        wav = self.tts_model.tts(text=text, speaker_wav=voice_sample, language=language)
        return wav, self.sample_rate