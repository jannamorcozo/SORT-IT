FROM python:3.11-slim

# Install system libs needed by Pillow / TFLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose port (Cloud Run uses PORT env var, default 8080)
ENV PORT=8080

# Start FastAPI app (backend/app.py defines app)
CMD exec uvicorn app:app --host 0.0.0.0 --port $PORT