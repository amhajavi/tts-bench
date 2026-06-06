import re
from pathlib import Path

import numpy as np
import torch
import torchaudio
from tqdm import tqdm

from tts_bench.models import MODELS
from tts_bench.metrics import METRICS


class Benchmark:
    def __init__(
        self,
        model_names: list[str],
        metric_names: list[str],
        voice_sample: str = None,
        demo_output_dir: str = None,
        language: str = "en",
        kokoro_voice_identifier: str = 'af_heart',
        vits_speaker: str = "p225",
    ):
        unknown_models = [n for n in model_names if n not in MODELS]
        if unknown_models:
            raise ValueError(f"Unknown model(s): {unknown_models}. Available: {list(MODELS)}")

        unknown_metrics = [n for n in metric_names if n not in METRICS]
        if unknown_metrics:
            raise ValueError(f"Unknown metric(s): {unknown_metrics}. Available: {list(METRICS)}")

        self.models = [MODELS[n](language=language) for n in tqdm(model_names, desc="Loading the models")]
        self.metrics = [METRICS[n]() for n in metric_names]
        self.voice_sample = voice_sample
        self.demo_output_dir = Path(demo_output_dir) if demo_output_dir else None
        self.kokoro_voice_identifier = kokoro_voice_identifier
        self.vits_speaker = vits_speaker
        
        self.synthesizer_kwargs = {
            "voice_sample": voice_sample,
            "kokoro_voice_identifier": kokoro_voice_identifier,
            "vits-speaker": vits_speaker, 
        }

    def run(self, texts: list[str]) -> list[dict]:
        results = []
        for model in tqdm(self.models, desc="Speech Generation Models:"):
            model.load_to_device()
            row = {
                "model": model.__class__.__name__,
                "scores": {},
            }
            for text in tqdm(texts, desc=f"{model.__class__.__name__}", leave=False):
                audio, sr = model.synthesize(
                        text=text,
                        **self.synthesizer_kwargs,
                    )
                for metric in self.metrics:
                    score = metric.compute(audio, text)
                    row["scores"].setdefault(metric.__class__.__name__, []).append(score)

                if self.demo_output_dir is not None:
                    row.setdefault("demo_audio", []).append(
                        str(self._save_audio(audio, sr, model.__class__.__name__, text))
                    )
            model.unload_from_device()
            results.append(row)
        return results

    def _save_audio(self, audio: np.ndarray, sr: int, model_name: str, text: str) -> Path:
        snippet = text.strip()[:50]
        filename = re.sub(r"[^\w\s-]", "", snippet).strip()
        filename = re.sub(r"\s+", "_", filename) or "audio"

        out_dir = self.demo_output_dir / model_name
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{filename}.wav"

        waveform = torch.tensor(np.array(audio, dtype=np.float32)).unsqueeze(0)
        torchaudio.save(str(out_path), waveform, sr)
        return out_path
