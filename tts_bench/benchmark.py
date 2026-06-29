import re
from pathlib import Path

import numpy as np
import torch
import torchaudio
from tqdm import tqdm

from tts_bench.models import MODELS
from tts_bench.models.loader import load_custom_model
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
        custom_model_paths: list[str] = None,
    ):
        registry = dict(MODELS)
        for spec in (custom_model_paths or []):
            name, cls = load_custom_model(spec)
            registry[name] = cls

        unknown_models = [n for n in model_names if n not in registry]
        if unknown_models:
            raise ValueError(f"Unknown model(s): {unknown_models}. Available: {list(registry)}")

        unknown_metrics = [n for n in metric_names if n not in METRICS]
        if unknown_metrics:
            raise ValueError(f"Unknown metric(s): {unknown_metrics}. Available: {list(METRICS)}")

        self.models = [registry[n](language=language) for n in tqdm(model_names, desc="Loading the models")]
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
        for model in self.models:
            print(f"\033[92m{model.__class__.__name__}\033[0m")
            model.load_to_device()
            row = {
                "model": model.__class__.__name__,
                "scores": {},
            }

            audio_outputs = []

            for text in tqdm(texts, desc=f"Generating audio for {model.__class__.__name__}"):
                audio, sr = model.synthesize(
                        text=text,
                        **self.synthesizer_kwargs,
                    )
                audio_outputs.append((audio, sr, text))
    
            for metric in tqdm(self.metrics, desc=f"Evaluating metrics for {model.__class__.__name__}"):
                metric.load_to_device()
                all_scores = []
                for index, (audio, sr, text) in enumerate(tqdm(audio_outputs, desc=f"Computing {metric.__class__.__name__} for {model.__class__.__name__}", leave=False)):
                    score = metric.compute(audio, text, sr=sr, reference=self.voice_sample)
                    row["scores"].setdefault(metric.__class__.__name__, {}).update({index: score})
                    score = np.reshape(score, (1,-1,))
                    all_scores+= [score]
                row["scores"][metric.__class__.__name__]["all"] = np.mean(all_scores), np.std(all_scores)

                
                metric.unload_from_device()

            if self.demo_output_dir is not None:
                for index, (audio, sr, text) in enumerate(tqdm(audio_outputs, desc=f"Saving audio for {model.__class__.__name__}")):
                    row.setdefault("demo_audio", {}).update({index: str(self._save_audio(audio, sr, model.__class__.__name__, text))})
            model.unload_from_device()
            results.append(row)
        return results

    def _save_audio(self, audio: np.ndarray, sr: int, model_name: str, text: str) -> Path:
        snippet = text.strip()[:50]
        filename = re.sub(r"[^\w\s-]", "", snippet).strip()
        filename = re.sub(r"\s+", "_", filename) or "audio"

        out_dir = self.demo_output_dir / "assets" / model_name
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{filename}.wav"

        waveform = torch.tensor(np.array(audio, dtype=np.float32)).unsqueeze(0)
        torchaudio.save(str(out_path), waveform, sr)
        return out_path
