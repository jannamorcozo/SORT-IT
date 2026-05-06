from fastapi import FastAPI

from google_credentials_setup import setup_google_credentials
from routes.predict import router as predict_router

# Set up Google credentials before anything uses Google SDKs
setup_google_credentials()

app = FastAPI(title="SORT-IT Backend")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(predict_router, prefix="/api")