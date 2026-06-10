# Register metrics here as they are implemented:
from tts_bench.metrics.text_based import WER, CER   

METRICS = {
    "wer": WER,
    "cer": CER,
}
