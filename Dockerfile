# Production Dockerfile for InsureAI Pro Platform
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and models
COPY . .

# Run ML pipeline if model artifacts not present (ensures reproducibility)
RUN python ml_pipeline.py

EXPOSE 5000

# Run with Gunicorn WSGI HTTP Server
CMD ["gunicorn", "backend.app:create_app()", "--bind", "0.0.0.0:5000", "--workers", "4"]
