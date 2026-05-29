from tts_bench.models.base import BaseTTSModel

from TTS.api import TTS

class XTTSWrapper(BaseTTSModel):
    def __init__(self):
        
        super(XTTSWrapper).__init__()
        
        self.tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
    
    def synthesize(self, text, voice_sample=None, language="en", **kwargs):
        wav = tts.tts(text="Hello world!", speaker_wav=voice_sample, language=language)
        return wav, self.tts_model.sr