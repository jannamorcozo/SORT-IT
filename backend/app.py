from fastapi import FastAPI

from routes.predict import router as predict_router

app = FastAPI(title="SORT-IT Backend")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(predict_router, prefix="/api")