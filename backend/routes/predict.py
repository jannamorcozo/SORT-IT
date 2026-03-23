from fastapi import APIRouter, File, UploadFile
import numpy as np

from core.config import STAGE2_LABELS, STAGE3_LABELS
from core.model_registry import get_stage3_model, stage1_model, stage2_model
from services.image import preprocess_image

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()
    with open("temp.jpg", "wb") as f:
        f.write(contents)

    img_array = preprocess_image("temp.jpg")

    pred1 = stage1_model.predict(img_array)
    if np.argmax(pred1) == 0:
        return {"recyclable": False, "message": "Non-Recyclable"}

    pred2 = stage2_model.predict(img_array)
    material = STAGE2_LABELS[np.argmax(pred2)]

    pred3 = get_stage3_model(material).predict(img_array)
    subcategory = STAGE3_LABELS[material][np.argmax(pred3)]

    return {"recyclable": True, "material": material, "subcategory": subcategory}
