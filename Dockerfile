# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port FastAPI runs on (Cloud Run will override or assign)
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run uvicorn to host the FastAPI application
CMD ["python", "main.py"]
