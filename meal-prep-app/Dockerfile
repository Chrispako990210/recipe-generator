# Stage 1: Build the Vue.js frontend
# FIX: Changed from 'alpine' to 'slim' to fix Windows network hangs
FROM node:18-slim AS frontend-builder

WORKDIR /frontend

# Copy package files
COPY frontend/package*.json ./

# FIX: increased timeout and forced registry to prevent stalls
RUN npm config set fetch-retry-maxtimeout 600000 \
    && npm config set fetch-retry-mintimeout 10000 \
    && npm install --no-audit

# Copy source files
COPY frontend/ .

# Build the Vue app
RUN npm run build

# Stage 2: Python runtime with FastAPI (No changes needed here)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application
COPY app/ .

# Copy the built frontend from the builder stage
COPY --from=frontend-builder /frontend/dist ./static

# Security setup
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]