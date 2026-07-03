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
        output_dir: str = None,
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
        self.output_dir = Path(output_dir) if output_dir else None
        self.kokoro_voice_identifier = kokoro_voice_identifier
        self.vits_speaker = vits_speaker
        
        self.synthesizer_kwargs = {
            "voice_sample": voice_sample,
            "kokoro_voice_identifier": kokoro_voice_identifier,
            "vits-speaker": vits_speaker, 
        }

    def run(self, texts: list[str]) -> list[dict]:
        
        results = {
            "models": [model.name for model in self.models],
            "metrics": [metric.__class__.__name__ for metric in self.metrics],
            "records": [],
        }
        
        for index, model in enumerate(self.models):
            print(f"\033[92m{model.name} ({index+1}/{len(self.models)})\033[0m")
            model.load_to_device()
            row = {
                "model": model.name, # cleaner access in the report templates
                "metrics": [metric.__class__.__name__ for metric in self.metrics], # cleaner access in the report templates
                "scores": {},
                "instances": {} 
            }

            for index, text in enumerate(tqdm(texts, desc=f"Generating audio for {model.name}")):
                audio, sr = model.synthesize(
                        text=text,
                        **self.synthesizer_kwargs,
                    )
                
                row["instances"][index] = {
                    "text": text,
                    "sr": sr,
                    "audio": audio,
                    "file": str(self._save_audio(audio, sr, model.name, text)).replace(str(self.output_dir), ""),
                    "duration": float(len(audio) / sr)
                }
    
            for metric in tqdm(self.metrics, desc=f"Evaluating metrics for {model.name}"):
                metric.load_to_device()
                all_scores = []
                for index, record in tqdm(row["instances"].items(), desc=f"Computing {metric.__class__.__name__} for {model.name}", leave=False):
                    audio = record["audio"]
                    text = record["text"]
                    sr = record["sr"]
                    score = metric.compute(audio, text, sr=sr, reference=self.voice_sample)
                    row["instances"][index][metric.__class__.__name__] = score
                    all_scores.append(score)
                row["scores"][metric.__class__.__name__] = np.mean(all_scores), np.std(all_scores)

                
                metric.unload_from_device()
            model.unload_from_device()
            results["records"].append(row)
        return results

    def _save_audio(self, audio: np.ndarray, sr: int, model_name: str, text: str) -> Path:
        snippet = text.strip()[:50]
        filename = re.sub(r"[^\w\s-]", "", snippet).strip()
        filename = re.sub(r"\s+", "_", filename) or "audio"

        out_dir = self.output_dir / "assets" / model_name
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{filename}.wav"

        waveform = torch.tensor(np.array(audio, dtype=np.float32)).unsqueeze(0)
        torchaudio.save(str(out_path), waveform, sr)
        return out_path
