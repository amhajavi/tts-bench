from tts_bench.models.base import BaseTTSModel
from tts_bench.models.xtts import XTTSWrapper
from tts_bench.models.yourtts import YourTTSWrapper
from tts_bench.models.kokoro import KokoroWrapper
from tts_bench.models.vits import VITSWrapper

MODELS = {
    "xtts": XTTSWrapper,
    "your-tts": YourTTSWrapper,
    "kokoro": KokoroWrapper,
    "vits": VITSWrapper,
}
