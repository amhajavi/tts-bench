# Register metrics here as they are implemented:
from tts_bench.metrics.text_based import WER, CER   
from tts_bench.metrics.utmosv2 import UTMOSV2

METRICS = {
    "wer": WER,
    "cer": CER,
    "utmosv2": UTMOSV2,
}
