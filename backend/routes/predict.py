from typing import Any, Dict, Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pydantic import BaseModel

from services.image import preprocess_image
from services.inference import classify_image

router = APIRouter(tags=["prediction"])


class StageResult(BaseModel):
    label: str
    confidence: float


class PredictionResponse(BaseModel):
    stage1: StageResult
    stage2: Optional[StageResult] = None
    stage3: Optional[StageResult] = None


@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)) -> Dict[str, Any]:
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG and PNG images are supported.",
        )

    file_bytes = await file.read()
    image_array = preprocess_image(file_bytes, target_size=(224, 224))

    result = classify_image(image_array)
    return result