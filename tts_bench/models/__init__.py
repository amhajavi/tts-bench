from tts_bench.models.xtts import XTTSWrapper
from tts_bench.models.yourtts import YourTTSWrapper
from tts_bench.models.kokoro import KokoroWrapper

MODELS = {
    "xtts": XTTSWrapper,
    "your-tts": YourTTSWrapper,
    "kokoro": KokoroWrapper,
}
