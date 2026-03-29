from io import BytesIO
from typing import Tuple

import numpy as np
from PIL import Image
from tensorflow.keras.applications import MobileNetV3Large
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

def preprocess_image(file_bytes: bytes, target_size: Tuple[int, int] = (224, 224)):
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    image = image.resize(target_size)

    # Create float32 array in HWC format, just like training
    arr = np.array(image, dtype=np.float32)

    # Use the same preprocess_input as in the notebook
    arr = preprocess_input(arr)

    # Add batch dimension (1, 224, 224, 3)
    return np.expand_dims(arr, axis=0)