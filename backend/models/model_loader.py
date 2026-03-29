from functools import lru_cache
from pathlib import Path
import os

from google.cloud import storage
from tensorflow.lite.python.interpreter import Interpreter
from config import get_settings

settings = get_settings()
CACHE_DIR = Path("cache/models")


def _download_model_from_gcs(object_path: str) -> Path:
    """
    Download a model from GCS to a local cache folder if not already cached.
    Returns local file path.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    local_path = CACHE_DIR / os.path.basename(object_path)

    if local_path.exists():
        return local_path

    client = storage.Client(project=settings.gcp_project_id)
    bucket = client.bucket(settings.gcs_model_bucket)
    blob = bucket.blob(object_path)
    blob.download_to_filename(str(local_path))

    return local_path


def _load_tflite_interpreter(object_path: str) -> Interpreter:
    local_path = _download_model_from_gcs(object_path)
    interpreter = Interpreter(model_path=str(local_path))
    interpreter.allocate_tensors()
    return interpreter


@lru_cache
def get_stage1_interpreter() -> Interpreter:
    return _load_tflite_interpreter(settings.model_stage1_path)


@lru_cache
def get_stage2_interpreter() -> Interpreter:
    return _load_tflite_interpreter(settings.model_stage2_path)


@lru_cache
def get_stage3_plastic_interpreter() -> Interpreter:
    return _load_tflite_interpreter(settings.model_stage3_plastic_path)


@lru_cache
def get_stage3_glass_interpreter() -> Interpreter:
    return _load_tflite_interpreter(settings.model_stage3_glass_path)


@lru_cache
def get_stage3_metal_interpreter() -> Interpreter:
    return _load_tflite_interpreter(settings.model_stage3_metal_path)


@lru_cache
def get_stage3_paper_interpreter() -> Interpreter:
    return _load_tflite_interpreter(settings.model_stage3_paper_path)

@lru_cache
def get_stage3_residual_interpreter() -> Interpreter:
    return _load_tflite_interpreter(settings.model_stage3_residual_path)