# backend/Dockerfile
FROM python:3.9-slim

# Install build tools and dependencies needed for gevent and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libev-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code into the container
COPY . .

# Expose port 8000 (if your app listens on 8000)
EXPOSE 8000

# Set the default command to run your app (adjust as needed)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
