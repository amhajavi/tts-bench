# tts-bench

**A modern, batteries-included evaluation library for open-source and API-based TTS models.**

`tts-bench` lets you evaluate and compare text-to-speech models in minutes — not hours. Point it at one or more models, give it a set of texts, and get back a structured report with audio playback and a comprehensive set of metrics you choose from.

```bash
pip install tts-bench
```

---

## Why tts-bench?

Evaluating TTS models is surprisingly painful. You either write one-off scripts per model, cobble together separate tools for each metric, or rely on benchmarks that are years out of date. `tts-bench` fixes that:

- **One interface for all models** — open-source (Kokoro, XTTS, YourTTS, VITS) and API-based (ElevenLabs, OpenAI) share the same evaluation API
- **Pick your metrics** — choose from a comprehensive library of intelligibility, naturalness, prosody, speaker, and signal metrics
- **Human-readable output** — an HTML report with inline audio playback so you can *hear* the differences, not just read numbers
- **Reproducible by default** — every run is logged with model versions, inputs, and environment info

---

## Quickstart

### Evaluate a single model

```python
from tts_bench import evaluate

results = evaluate(
    model="kokoro",
    texts=[
        "The quick brown fox jumps over the lazy dog.",
        "Call 1-800-555-0199 to speak with an agent.",
        "Dr. Smith confirmed the diagnosis: type 2 diabetes.",
    ],
    metrics=["wer", "utmos", "pitch_rmse"]
)

results.save_report("report.html")
```

### Compare two models side by side

```python
from tts_bench import compare

report = compare(
    models=["kokoro", "vits"],
    texts="my_eval_texts.txt",  # one sentence per line
    metrics=["wer", "cer", "utmos", "speaker_sim", "stress_pass_rate"]
)

report.save_report("comparison.html")
print(report.summary())
```

```
┌──────────────────────┬────────┬────────┐
│ Metric               │ Kokoro │ VITS   │
├──────────────────────┼────────┼────────┤
│ WER ↓                │ 0.031  │ 0.048  │
│ CER ↓                │ 0.018  │ 0.031  │
│ UTMOS ↑              │ 4.21   │ 3.87   │
│ Speaker Sim ↑        │ 0.91   │ 0.84   │
│ Stress Pass Rate ↑   │ 91%    │ 76%    │
└──────────────────────┴────────┴────────┘
```

### Run from the command line

```bash
tts-bench run --models kokoro vits --metrics wer utmos speaker_sim --input texts.txt --output report.html
```

---

## Metrics

`tts-bench` takes a `metrics=` argument everywhere. Pass a list of metric keys to run only what you need. Below is the full catalogue, organized by category.

---

### Intelligibility

These metrics measure whether the model actually says what you asked it to say.

| Key | Metric | What it measures | Reference needed? |
|---|---|---|---|
| `wer` | Word Error Rate | Word-level transcription accuracy via Whisper ASR | No |
| `cer` | Character Error Rate | Character-level transcription accuracy via Whisper ASR | No |
| `ttscore_int` | TTScore-Int | Reference-free intelligibility via discrete speech token prediction | No |

---

### Naturalness & Perceived Quality

These metrics estimate how natural and pleasant the speech sounds, without needing human listeners.

| Key | Metric | What it measures | Reference needed? |
|---|---|---|---|
| `utmos` | UTMOS | Predicted MOS naturalness score (1–5) | No |
| `utmos_v2` | UTMOSv2 | Improved MOS predictor, stronger on modern systems | No |
| `nisqa` | NISQA-MOS | Non-intrusive speech quality assessment | No |
| `dnsmos` | DNSMOS | Microsoft's non-intrusive MOS predictor | No |
| `squim_mos` | SQUIM-MOS | Torchaudio's MOS predictor, grounded by non-matching reference | Optional |
| `ttsds2` | TTSDS2 | Distributional quality score across prosody, speaker, and intelligibility — strongest correlation with human MOS of any automatic metric | No |

---

### Prosody

These metrics measure the expressiveness, rhythm, and pitch characteristics of the output.

| Key | Metric | What it measures | Reference needed? |
|---|---|---|---|
| `pitch_rmse` | F0 RMSE | Pitch contour error vs. reference speech | Yes |
| `duration_error` | Duration Prediction Error | Phoneme/word duration accuracy vs. reference | Yes |
| `prosody_diversity` | Prosody Diversity Score | Whether the model produces varied prosody across different inputs (not flat/robotic) | No |
| `ttscore_pro` | TTScore-Pro | Reference-free prosody evaluation via pitch token prediction | No |
| `speechbertscore` | SpeechBERTScore | Reference-aware evaluation leveraging NLP-style embedding comparison | Yes |

---

### Speaker & Voice

These metrics are most relevant for voice cloning and zero-shot TTS scenarios.

| Key | Metric | What it measures | Reference needed? |
|---|---|---|---|
| `speaker_sim` | Speaker Similarity (ECAPA-TDNN) | Cosine similarity between output and reference speaker embeddings | Yes |
| `speaker_sim_xvec` | Speaker Similarity (x-vector) | x-vector based speaker similarity | Yes |
| `speaker_sim_rawnet` | Speaker Similarity (RawNet3) | RawNet3-based speaker similarity | Yes |

---

### Signal Quality

These are classical signal-level metrics, useful for reference-based comparisons or when ground truth audio is available.

| Key | Metric | What it measures | Reference needed? |
|---|---|---|---|
| `mcd` | Mel-Cepstral Distortion | Spectral distance between synthetic and reference audio | Yes |
| `pesq` | PESQ | Perceptual evaluation of speech quality, widely used in telecom | Yes |
| `stoi` | STOI | Short-time objective intelligibility (0–100%) | Yes |
| `estoi` | ESTOI | Extended STOI, better for low-intelligibility conditions | Yes |

---

### Robustness (Stress Testing)

These are not single numeric metrics but pass/fail evaluations across curated stress-test input categories.

| Key | Category | What it tests |
|---|---|---|
| `stress_pass_rate` | Overall stress pass rate | Aggregate pass rate across all categories below |
| `stress_numbers` | Numbers & currency | `"The total is $1,492.50."` |
| `stress_abbreviations` | Abbreviations & acronyms | `"She has a PhD from MIT."` |
| `stress_foreign` | Foreign words & names | `"The prix fixe menu features coq au vin."` |
| `stress_punctuation` | Heavy punctuation | `"Wait — are you serious?! That's... unexpected."` |
| `stress_long` | Long-form text | 100+ word passages testing consistency over time |
| `stress_repetition` | Repeated phrases | Inputs that trigger hallucination in LLM-based TTS models |
| `stress_homophones` | Homophones & ambiguous spelling | `"They're going to their house over there."` |

---

### Convenience Bundles

Not sure where to start? Use a pre-defined bundle:

| Bundle | Metrics included |
|---|---|
| `"quick"` | `wer`, `utmos` |
| `"standard"` | `wer`, `cer`, `utmos`, `speaker_sim`, `stress_pass_rate` |
| `"full"` | All non-reference metrics |
| `"reference"` | All metrics (requires reference audio) |

```python
results = evaluate(model="kokoro", texts=my_texts, metrics="standard")
```

---

## Stress-Test Suite

The built-in stress-test suite is a curated set of inputs that commonly break TTS models in practice. You can use it as-is, extend it, or bring your own:

```python
from tts_bench import evaluate
from tts_bench.suites import STRESS_TEST, load_suite

# Use the built-in suite
results = evaluate(model="kokoro", texts=STRESS_TEST, metrics="standard")

# Load your own
results = evaluate(model="kokoro", texts=load_suite("my_suite.txt"), metrics="standard")
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
from tts_bench import evaluate, compare
from my_model import MyCustomModel

# Evaluate a single custom model
results = evaluate(
    model=MyCustomModel(),
    texts=[
        "The quick brown fox jumps over the lazy dog.",
        "She has a PhD from MIT.",
    ],
    metrics=["wer", "utmos"]
)
results.save_report("report.html")

# Compare a custom model against a built-in one
report = compare(
    models=[MyCustomModel(), "kokoro"],
    texts="eval_texts.txt",
    metrics="standard"
)
print(report.summary())
```

You can also use a custom model from the CLI with `--custom-model <file>::<ClassName>`:

```bash
tts-bench run \
  --custom-model my_model.py::SilentModel \
  --models SilentModel \
  --metrics wer utmosv2 \
  --suit stress_test
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

XTTS, YourTTS, and VITS are all available via the `coqui-tts` package. Kokoro uses the `kokoro` package.

### API-based

| Provider | Key | Status |
|---|---|---|
| ElevenLabs | `elevenlabs` | 🔜 Coming soon |
| OpenAI TTS | `openai` | 🔜 Coming soon |
| Cartesia | `cartesia` | 🔜 Coming soon |

Want a model added? [Open an issue](https://github.com/amhajavi/tts-bench/issues).

---

## Installation

Requires Python 3.11+.

```bash
pip install tts-bench
```

For local model inference, install with the `local` extra:

```bash
pip install tts-bench[local]
```

---

## Contributing

Contributions are very welcome — especially new model adapters, metrics, and stress-test inputs.

```bash
git clone https://github.com/amhajavi/tts-bench.git
cd tts-bench
uv sync
uv run pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Roadmap

- [ ] ElevenLabs and OpenAI TTS adapters
- [ ] Hallucination detection metric (repeated/dropped words)
- [ ] Multilingual stress-test suite
- [ ] CI benchmark runner (run on every model release)
- [ ] LLM-as-judge integration for subjective scoring

---

## License

MIT