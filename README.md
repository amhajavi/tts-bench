# tts-bench

**A modern, batteries-included evaluation library for open-source and API-based TTS models.**

`tts-bench` is a passion project that may become useful for anyone who wants to evaluate Text-to-Speech models and compare them with each other. There are a few models available right now by default but the beauty of it is that it is very easy to add your model to the mix. It is by no means a complete project and it is still growing. All the contributions are welcome (Please look into `CONTRIBUTING.md` for the ways to contribute or even just use the tool and give me a feedback on what you would want to see on it).

```bash
pip install tts-bench
```

## Optional Dependencies

Some metrics require packages not available on PyPI and must be installed manually:

| Metric | Package | Install command |
|---|---|---|
| `utmos` | UTMOSv2 | `pip install git+https://github.com/sarulab-speech/UTMOSv2.git` |

---

## Why tts-bench?

Evaluating TTS models is surprisingly painful. You either write one-off scripts per model, cobble together separate tools for each metric, or rely on benchmarks that are years out of date. `tts-bench` is trying to fix that:

- **One interface for all models** — open-source (Kokoro, XTTS, YourTTS, VITS) and soon to be added API-based (ElevenLabs, OpenAI) share the same evaluation API. You can even add your own very eaily
- **Pick your metrics** — choose from a growing library of intelligibility, naturalness, speaker, and signal metrics
- **Human-readable output** — an HTML report with inline audio playback so you can *hear* the differences, not just read numbers

---

## Quickstart

### Evaluate a single model

```python
from tts_bench.benchmark import Benchmark
from tts_bench.report import generate_report

bench = Benchmark(
    model_names=["kokoro"],
    metric_names=["wer", "utmos"],
    output_dir="output",
)

texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Call 1-800-555-0199 to speak with an agent.",
    "Dr. Smith confirmed the diagnosis: type 2 diabetes.",
]

results = bench.run(texts)
generate_report(results, "output")
```

### Compare two models side by side

```python
from tts_bench.benchmark import Benchmark
from tts_bench.report import generate_report

bench = Benchmark(
    model_names=["kokoro", "vits"],
    metric_names=["wer", "cer", "utmosv2", "speaker_similarity"],
    output_dir="output",
)

with open("my_eval_texts.txt") as f:
    texts = [line for line in f.read().splitlines() if line.strip()]

results = bench.run(texts)
generate_report(results, "output")
```

### Run from the command line

```bash
tts-bench run --models kokoro vits --metrics wer utmosv2 speaker_similarity --input texts.txt --output-dir output
```

---

## Metrics

`tts-bench` takes a `metrics=` argument everywhere. Pass a list of metric keys to run only what you need. Below is the full catalogue, organized by category.

---

### Intelligibility

These metrics measure whether the model actually says what you asked it to say.

| Key | Metric | What it measures | Reference needed? | Status |
|---|---|---|---|---|
| `wer` | Word Error Rate | Word-level transcription accuracy via Whisper ASR | No | ✅ |
| `cer` | Character Error Rate | Character-level transcription accuracy via Whisper ASR | No | ✅ |
| `ttscore_int` | TTScore-Int | Reference-free intelligibility via discrete speech token prediction | No | 🔜 |

---

### Naturalness & Perceived Quality

These metrics estimate how natural and pleasant the speech sounds, without needing human listeners.

| Key | Metric | What it measures | Reference needed? | Status |
|---|---|---|---|---|
| `utmosv2` | UTMOSv2 | Improved MOS predictor, stronger on modern systems | No | ✅ |
| `dnsmos` | DNSMOS | Microsoft's non-intrusive MOS predictor | No | ✅ |
| `nisqa` | NISQA-MOS | Non-intrusive speech quality assessment | No | 🔜 |
| `squim_mos` | SQUIM-MOS | Torchaudio's MOS predictor, grounded by non-matching reference | Optional | 🔜 |
| `ttsds2` | TTSDS2 | Distributional quality score across prosody, speaker, and intelligibility — strongest correlation with human MOS of any automatic metric | No | 🔜 |

---

### Prosody

These metrics measure the expressiveness, rhythm, and pitch characteristics of the output.

| Key | Metric | What it measures | Reference needed? | Status |
|---|---|---|---|---|
| `pitch_rmse` | F0 RMSE | Pitch contour error vs. reference speech | Yes | 🔜 |
| `duration_error` | Duration Prediction Error | Phoneme/word duration accuracy vs. reference | Yes | 🔜 |
| `prosody_diversity` | Prosody Diversity Score | Whether the model produces varied prosody across different inputs (not flat/robotic) | No | 🔜 |
| `ttscore_pro` | TTScore-Pro | Reference-free prosody evaluation via pitch token prediction | No | 🔜 |
| `speechbertscore` | SpeechBERTScore | Reference-aware evaluation leveraging NLP-style embedding comparison | Yes | 🔜 |

---

### Speaker & Voice

These metrics are most relevant for voice cloning and zero-shot TTS scenarios.

| Key | Metric | What it measures | Reference needed? | Status |
|---|---|---|---|---|
| `speaker_similarity` | Speaker Similarity (ECAPA-TDNN) | Cosine similarity between output and reference speaker embeddings | Yes | ✅ |
| `speaker_sim_xvec` | Speaker Similarity (x-vector) | x-vector based speaker similarity | Yes | 🔜 |
| `speaker_sim_rawnet` | Speaker Similarity (RawNet3) | RawNet3-based speaker similarity | Yes | 🔜 |

---

### Signal Quality

These are classical signal-level metrics, useful for reference-based comparisons or when ground truth audio is available.

| Key | Metric | What it measures | Reference needed? | Status |
|---|---|---|---|---|
| `mcd` | Mel-Cepstral Distortion | Spectral distance between synthetic and reference audio | Yes | 🔜 |
| `pesq` | PESQ | Perceptual evaluation of speech quality, widely used in telecom | Yes | 🔜 |
| `stoi` | STOI | Short-time objective intelligibility (0–100%) | Yes | 🔜 |
| `estoi` | ESTOI | Extended STOI, better for low-intelligibility conditions | Yes | 🔜 |

---

### Robustness (Stress Testing)

| Key | Metric | What it measures | Reference needed? | Status |
|---|---|---|---|---|
| `stress_pass_rate` | Stress Pass Rate | Aggregate pass rate across the built-in stress suite | No | ✅ |

---

## Stress-Test Suite

The built-in stress-test suite is a curated set of inputs that commonly break TTS models in practice. You can use it as-is, extend it, or bring your own.

| Suite name | Category | Status |
|---|---|---|
| `stress_test` | Full stress test | ✅ |
| `stress_light` | Lightweight stress test | ✅ |
| `stress_numbers` | Numbers & currency | 🔜 |
| `stress_abbreviations` | Abbreviations & acronyms | 🔜 |
| `stress_foreign` | Foreign words & names | 🔜 |
| `stress_punctuation` | Heavy punctuation | 🔜 |
| `stress_long` | Long-form text | 🔜 |
| `stress_repetition` | Repeated phrases | 🔜 |
| `stress_homophones` | Homophones & ambiguous spelling | 🔜 |

```python
from tts_bench.benchmark import Benchmark
from tts_bench.report import generate_report
from tts_bench.suites import load_suite

# Use the built-in suite
texts = load_suite("stress_test")

# Or provide your own text file via --input on the CLI,
# or read it manually:
with open("my_suite.txt") as f:
    texts = [line for line in f.read().splitlines() if line.strip()]

bench = Benchmark(model_names=["kokoro"], metric_names=["wer", "utmosv2"], output_dir="output")
results = bench.run(texts)
generate_report(results, "output")
```

---

## Custom Models

You can benchmark any TTS model — not just the built-in ones — by subclassing `BaseTTSModel` and passing your class directly to `evaluate` or `compare`.

### How a custom model file should look

```python
# my_model.py
import numpy as np
from tts_bench.models import BaseTTSModel


class MyCustomModel(BaseTTSModel):

    sample_rate = 22050  # output sample rate in Hz

    def __init__(self, **kwargs):
        super().__init__()
        # load your model weights / initialize your API client here

    def synthesize(self, text: str, **kwargs) -> tuple[np.ndarray, int]:
        """
        Must return a tuple of (audio_samples, sample_rate).
        audio_samples — 1-D float32 numpy array of PCM audio.
        sample_rate   — integer sample rate in Hz.
        """
        # replace with your actual synthesis call
        samples = np.zeros(self.sample_rate * 1, dtype=np.float32)
        return samples, self.sample_rate
```

**Rules:**
- Subclass `tts_bench.models.BaseTTSModel`.
- Set the `sample_rate` class attribute to match your model's output.
- Implement `synthesize(text, **kwargs)` and return `(np.ndarray, int)`.
- Optionally override `load_to_device()` / `unload_from_device()` if your model uses PyTorch and you want automatic GPU memory management during multi-model runs.

### Usage

```python
from tts_bench.benchmark import Benchmark
from tts_bench.report import generate_report

# Evaluate a single custom model
bench = Benchmark(
    model_names=["MyCustomModel"],
    metric_names=["wer", "utmosv2"],
    output_dir="output",
    custom_model_paths=["my_model.py::MyCustomModel"],
)
results = bench.run([
    "The quick brown fox jumps over the lazy dog.",
    "She has a PhD from MIT.",
])
generate_report(results, "output")

# Compare a custom model against a built-in one
bench = Benchmark(
    model_names=["MyCustomModel", "kokoro"],
    metric_names=["wer", "cer", "utmosv2", "speaker_similarity"],
    output_dir="output",
    custom_model_paths=["my_model.py::MyCustomModel"],
)
with open("eval_texts.txt") as f:
    texts = [line for line in f.read().splitlines() if line.strip()]
results = bench.run(texts)
generate_report(results, "output")
```

You can also use a custom model from the CLI with `--custom-model <file>::<ClassName>`:

```bash
tts-bench run \
  --custom-model my_model.py::SilentModel \
  --models SilentModel \
  --metrics wer utmos \
  --suit stress_test \
  --output-dir output
```

`--custom-model` registers the class from the given file, and `--models` then refers to it by class name alongside any built-in model keys.

---

## Supported Models

> **System requirement:** `espeak-ng` must be installed before using any local model.
> - Ubuntu/Debian: `sudo apt-get install espeak-ng`
> - macOS: `brew install espeak-ng`
> - Windows: `winget install espeak-ng`

### Open-Source (local inference)

| Model | Key | Character | Status |
|---|---|---|---|
| Kokoro-82M | `kokoro` | Lightweight, modern, Apache 2.0 | ✅ Supported |
| XTTS v2 | `xtts` | Multilingual (17 langs), voice cloning | ✅ Supported |
| YourTTS | `yourtts` | Zero-shot voice cloning from 3s clip | ✅ Supported |
| VITS (VCTK) | `vits` | Deterministic, 109 English speakers | ✅ Supported |
| Parler TTS | `parler` | Prompted style control | 🔜 Coming soon |
| StyleTTS2 | `styletts2` | High naturalness, style transfer | 🔜 Coming soon |
| FishAudio | `fish` | Realistic voice cloning | 🔜 Coming soon |
| CosyVoice | `cosyvoice` | Multilingual, instruction-following TTS | 🔜 Coming soon |
| IndexTTS | `indextts` | High-fidelity zero-shot voice cloning | 🔜 Coming soon |

XTTS, YourTTS, and VITS are all available via the `coqui-tts` package. Kokoro uses the `kokoro` package.

### API-based

| Provider | Key | Status |
|---|---|---|
| ElevenLabs | `elevenlabs` | 🔜 Coming soon |
| OpenAI TTS | `openai` | 🔜 Coming soon |
| Cartesia | `cartesia` | 🔜 Coming soon |
| Gemini TTS | `gemini` | 🔜 Coming soon |

Want a model added? [Open an issue](https://github.com/amhajavi/tts-bench/issues).

---

## Installation

Requires Python 3.11+.

```bash
pip install tts-bench
```
or 


```bash
git clone https://github.com/amhajavi/tts-bench.git
cd tts-bench
uv sync
```

---

## Contributing

Contributions are very welcome — especially new model adapters, metrics, and stress-test inputs.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Roadmap

- [ ] ElevenLabs, Gemini, Cartesia, and OpenAI TTS adapters
- [ ] Hallucination detection metric (repeated/dropped words)
- [ ] Automated app builder for subjective scoring
- [ ] Multilingual stress-test suite
- [ ] ... 

---

## License

MIT