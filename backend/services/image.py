from io import BytesIO
from typing import Tuple

import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

def preprocess_image(file_bytes: bytes, target_size: Tuple[int, int] = (224, 224)):
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    resample_mode = Image.Resampling.BILINEAR if hasattr(Image, "Resampling") else Image.BILINEAR
    image = image.resize(target_size, resample=resample_mode)

    # Convert to float32 HWC numpy array
    arr = np.array(image, dtype=np.float32)

    # Normalize with MobileNetV3 preprocessing (same as training)
    arr = preprocess_input(arr)

    # Return batched tensor shape (1, H, W, C)
    return np.expand_dims(arr, axis=0)