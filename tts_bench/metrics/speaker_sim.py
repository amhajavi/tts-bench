import torch
import numpy as np

import torchaudio
import torchmetrics.functional.pairwise.cosine as cosine_similarity
from speechbrain.inference.speaker import SpeakerRecognition

from tts_bench.metrics.base import BaseMetric

from torchaudio.transforms import Resample

class SpeakerSimilarity(BaseMetric):
    
    model = None
    
    def __init__(self):
        pass
    
    def compute(self, audio:np.ndarray, text: str, reference: np.ndarray = None, sr: int= 16000) -> float:
        if self.model is None:
            raise ValueError("Model is not loaded. Please call load_to_device() before computing metrics.")
        # every metric must have this implemented
        # Transcribe audio using faster-whisper
        audio = torch.reshape(audio, ( 1,-1,))
        reference, reference_sr = torchaudio.load(reference)
        reference = torch.reshape(reference, ( 1,-1,))
        reference_resampler = Resample(orig_freq=reference_sr, new_freq=16000)
        reference = reference_resampler(reference)

        if sr != 16000:
            audio_resampler = Resample(orig_freq=sr, new_freq=16000)
            audio = audio_resampler(audio)

        score, _ = self.model.verify_batch(wavs1 = reference, 
                                           wavs2 = audio)

        
        return score.cpu().numpy()[0]

    def load_to_device(self, device: str = "cuda"):
        self.model = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb", 
            savedir="pretrained_models/spkrec-ecapa-voxceleb"
        )
        self.model.to(device)
    
    def unload_from_device(self):
        self.model = None
        torch.cuda.empty_cache()