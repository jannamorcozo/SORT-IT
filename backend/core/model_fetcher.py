import os
import shutil
import tempfile
import urllib.request

from core.config import MODEL_DOWNLOAD_TIMEOUT_SECONDS


def download_if_missing(local_path: str, remote_url: str) -> None:
    if os.path.exists(local_path):
        return

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Write to a temp file first, then move atomically on success.
    fd, temp_path = tempfile.mkstemp(suffix=".keras", dir=os.path.dirname(local_path))
    os.close(fd)

    try:
        with urllib.request.urlopen(remote_url, timeout=MODEL_DOWNLOAD_TIMEOUT_SECONDS) as response:
            with open(temp_path, "wb") as out_file:
                shutil.copyfileobj(response, out_file)
        os.replace(temp_path, local_path)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise
