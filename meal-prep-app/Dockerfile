# Stage 1: Build the Vue.js frontend
FROM node:18 AS builder

WORKDIR /frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .

# Build the Vue app
RUN npm run build

# Stage 2: Python runtime with FastAPI
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application
COPY app/ .

# Copy the built frontend from the builder stage
COPY --from=builder /frontend/dist ./static

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
