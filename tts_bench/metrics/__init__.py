# Register metrics here as they are implemented:
from tts_bench.metrics.text_based import WER, CER   
from tts_bench.metrics.utmosv2 import UTMOSV2
from tts_bench.metrics.dnsmos import DNSMOS

METRICS = {
    "wer": WER,
    "cer": CER,
    "utmosv2": UTMOSV2,
    "dnsmos": DNSMOS,
}
