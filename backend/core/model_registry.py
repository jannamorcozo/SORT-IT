import os
import threading

from tensorflow.keras.models import load_model

from core.config import MODEL_FILENAMES, MODEL_PATH, MODEL_URLS
from core.model_fetcher import download_if_missing


_stage3_models: dict[str, object] = {}
_stage3_lock = threading.Lock()


def _ensure_model_available(model_key: str) -> str:
    filename = MODEL_FILENAMES[model_key]
    local_path = os.path.join(MODEL_PATH, filename)

    if os.path.exists(local_path):
        return local_path

    remote_url = MODEL_URLS.get(model_key, "").strip()
    if not remote_url:
        raise FileNotFoundError(
            f"Missing model '{filename}'. Add file locally or set URL env for {model_key}."
        )

    download_if_missing(local_path, remote_url)
    return local_path


def get_stage3_model(material: str):
    model_key = f"stage3_{material}"

    cached = _stage3_models.get(material)
    if cached is not None:
        return cached

    with _stage3_lock:
        cached = _stage3_models.get(material)
        if cached is not None:
            return cached

        local_path = _ensure_model_available(model_key)
        loaded = load_model(local_path)
        _stage3_models[material] = loaded
        return loaded


stage1_model = load_model(_ensure_model_available("stage1"))
stage2_model = load_model(_ensure_model_available("stage2"))
