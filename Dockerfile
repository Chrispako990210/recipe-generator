# Stage 1: Build Vue frontend
FROM node:18 AS frontend-builder

WORKDIR /build

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY index.html vite.config.js ./
COPY src ./src

# Build the frontend
RUN npm run build

# Stage 2: Python backend with FastAPI
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY main.py recipes.json ./

# Copy built frontend from stage 1
COPY --from=frontend-builder /build/dist ./static

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
