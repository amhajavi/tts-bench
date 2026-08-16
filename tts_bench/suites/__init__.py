import importlib.resources
from pathlib import Path

BUILTIN_SUITES = {
    "stress_test": Path(__file__).parent / "stress_test.txt",
    "stress_light": Path(__file__).parent / "stress_light.txt",
}


def load_suite(name: str) -> list[str]:
    if name not in BUILTIN_SUITES:
        raise ValueError(f"Unknown suite: '{name}'. Available: {list(BUILTIN_SUITES)}")
    return [line for line in BUILTIN_SUITES[name].read_text().splitlines() if line.strip()]
