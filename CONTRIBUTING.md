# Contributing to tts-bench

Thank you for taking the time to contribute! All contributions are welcome — bug reports, feature requests, new model adapters, new metrics, stress-test inputs, and documentation improvements.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting a Pull Request](#submitting-a-pull-request)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Adding a Model](#adding-a-model)
- [Adding a Metric](#adding-a-metric)
- [Coding Guidelines](#coding-guidelines)
- [Running Tests](#running-tests)

---

## Code of Conduct

Be respectful and constructive. This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. Harassment of any kind will not be tolerated.

---

## Getting Started

1. [Fork the repository](https://github.com/amhajavi/tts-bench/fork) on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/tts-bench.git
   cd tts-bench
   ```
3. Set up the development environment (see [Development Setup](#development-setup)).
4. Create a branch for your change:
   ```bash
   git checkout -b feat/my-new-feature
   ```
5. Make your changes, add tests, and open a pull request.

---

## How to Contribute

### Reporting Bugs

Before opening an issue, please search existing issues to avoid duplicates. When filing a bug report, include:

- A clear, descriptive title.
- Steps to reproduce the problem.
- Expected vs. actual behaviour.
- Your Python version, OS, and relevant package versions (`pip show tts-bench`).
- A minimal code snippet or error traceback, if applicable.

### Suggesting Features

Open a [GitHub issue](https://github.com/amhajavi/tts-bench/issues) with the label `enhancement`. Describe:

- The problem you are trying to solve.
- Your proposed solution or API.
- Any alternatives you have considered.

### Submitting a Pull Request

- Keep PRs focused — one feature or fix per PR.
- Reference the related issue in the PR description (e.g. `Closes #42`).
- Make sure all tests pass before requesting a review.
- Update the README if your change affects the public interface or adds a new model/metric.

---

## Development Setup

Requires Python 3.11+. The project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
pip install uv          # if you don't have uv yet
uv sync                 # install all dependencies including dev extras
```

---

## Project Structure

```
tts_bench/
├── benchmark.py        # Benchmark orchestration
├── report.py           # HTML report generation
├── cli/                # Click CLI definitions
├── metrics/            # Metric implementations
│   ├── base.py         # BaseMetric abstract class
│   ├── registry.py     # METRICS registry
│   └── ...
├── models/             # TTS model adapters
│   ├── base.py         # BaseTTSModel abstract class
│   ├── loader.py       # Custom model loader
│   └── ...
├── suites/             # Built-in stress-test text files
└── templates/          # Jinja2 HTML report templates
```

---

## Adding a Model

1. Create a new file under `tts_bench/models/`, e.g. `mymodel.py`.
2. Subclass `BaseTTSModel` and implement `synthesize`:

   ```python
   import numpy as np
   from tts_bench.models.base import BaseTTSModel

   class MyModel(BaseTTSModel):
       name = "mymodel"
       sample_rate = 22050

       def __init__(self, **kwargs):
           super().__init__(**kwargs)
           # initialise your model here

       def synthesize(self, text: str, **kwargs) -> tuple[np.ndarray, int]:
           # return (audio_array, sample_rate)
           ...
   ```

3. Register the model in `tts_bench/models/__init__.py`:

   ```python
   from tts_bench.models.mymodel import MyModel

   MODELS = {
       ...
       "mymodel": MyModel,
   }
   ```

4. Add the model to the Supported Models table in `README.md`.
5. Add at least a smoke test in `test/test_modules.py`.

---

## Adding a Metric

1. Create a new file under `tts_bench/metrics/`, e.g. `mymetric.py`.
2. Subclass `BaseMetric` and implement `compute`:

   ```python
   from tts_bench.metrics.base import BaseMetric

   class MyMetric(BaseMetric):
       def compute(self, audio: "np.ndarray", sr: int, text: str, **kwargs) -> float:
           ...
   ```

3. Register the metric in `tts_bench/metrics/__init__.py`:

   ```python
   from tts_bench.metrics.mymetric import MyMetric

   METRICS = {
       ...
       "mymetric": MyMetric,
   }
   ```

4. Add the metric to the Metrics table in `README.md` with the correct status (✅ or 🔜).
5. Add tests in `test/test_metrics.py`.

---

## Coding Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/). Use `ruff` for linting if available.
- Type-annotate all public functions and methods.
- Keep commits small and focused with clear messages (`feat:`, `fix:`, `docs:`, `chore:`).
- Do not commit model weights, large audio files, or secrets.

---

## Running Tests

```bash
uv run pytest
```

To run a specific file:

```bash
uv run pytest test/test_metrics.py
```
