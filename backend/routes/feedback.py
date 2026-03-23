from fastapi import APIRouter, Form

from core.firebase import db

router = APIRouter()

@router.post("/feedback")
async def feedback(predicted: str = Form(...), correct: str = Form(...)):
    db.collection("feedback").add({"predicted": predicted, "correct": correct})
    return {"status": "success"}
