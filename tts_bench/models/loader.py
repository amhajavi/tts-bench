import importlib.util
import inspect
from pathlib import Path

from tts_bench.models.base import BaseTTSModel


def load_custom_model(spec: str) -> tuple[str, type]:
    """Load a BaseTTSModel subclass from a file path.

    spec format:
        /path/to/file.py           — auto-detect single subclass
        /path/to/file.py::ClassName — load a specific class by name

    Returns (name, cls) where name is the class name used to register the model.
    Raises ValueError with a clear message on any error.
    """
    if "::" in spec:
        file_path, class_name = spec.rsplit("::", 1)
    else:
        file_path, class_name = spec, None

    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"Custom model file not found: {file_path}")
    if not path.suffix == ".py":
        raise ValueError(f"Custom model file must be a .py file: {file_path}")

    module_name = path.stem
    import_spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(import_spec)
    try:
        import_spec.loader.exec_module(module)
    except Exception as e:
        raise ValueError(f"Failed to import {file_path}: {e}") from e

    subclasses = [
        obj
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, BaseTTSModel) and obj is not BaseTTSModel and obj.__module__ == module_name
    ]

    if class_name:
        cls = getattr(module, class_name, None)
        if cls is None:
            raise ValueError(f"Class '{class_name}' not found in {file_path}")
        if not (inspect.isclass(cls) and issubclass(cls, BaseTTSModel)):
            raise ValueError(f"'{class_name}' in {file_path} does not subclass BaseTTSModel")
    else:
        if len(subclasses) == 0:
            raise ValueError(f"No BaseTTSModel subclass found in {file_path}")
        if len(subclasses) > 1:
            names = [c.__name__ for c in subclasses]
            raise ValueError(
                f"Multiple BaseTTSModel subclasses found in {file_path}: {names}. "
                f"Specify one with file.py::ClassName"
            )
        cls = subclasses[0]

    return cls.__name__, cls
