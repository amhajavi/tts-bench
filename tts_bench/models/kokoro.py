from tts_bench.models.base import BaseTTSModel
import torch
from kokoro import KPipeline

language_codes = {
    "en": "a",
    "fr": "f",
    "hi": "h"
}

class KokoroWrapper(BaseTTSModel):
    
    name = "Kokoro"
    sample_rate = 24000
    
    def __init__(self, **kwargs):
        super(KokoroWrapper).__init__()
        self.language = kwargs.get("language", "en")
        self.tts_model = KPipeline(
                repo_id="hexgrad/Kokoro-82M",
                lang_code=language_codes[self.language]
            )
        
    def synthesize(self, text, **kwargs):
        voice_identifier = kwargs.get("kokoro_voice_identifier", None)
        generator = self.tts_model(text, voice=voice_identifier)
        
        wav = []
        
        for i, (gs, ps, audio) in enumerate(generator):
            wav += audio
        wav = torch.tensor(wav)
        return wav, self.sample_rate
    
    def load_to_device(self):
        # this wapper of kokoro does not support GPU/CPU inference transfer as of now
        pass
    
    def unload_from_device(self):
        # this wapper of kokoro does not support GPU/CPU inference transfer as of now
        pass