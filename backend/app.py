from fastapi import FastAPI

from routes.feedback import router as feedback_router
from routes.predict import router as predict_router

app = FastAPI(title="SORT-IT Backend")


@app.get("/health")
async def health_check():
	return {"status": "ok"}

app.include_router(predict_router)
app.include_router(feedback_router)