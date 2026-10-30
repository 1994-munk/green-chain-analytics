# Use a lightweight official Python base image for the app runtime.
FROM python:3.11-slim

# Prevent Python from writing .pyc files and allow unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory inside the container.
WORKDIR /app

# Install OS-level build dependencies required by some Python packages.
# This is especially useful for database drivers and scientific libraries.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency file first to leverage Docker layer caching.
COPY requirements.txt ./

# Upgrade pip and install Python dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full application source code into the image.
COPY . .

# Expose the FastAPI service port.
EXPOSE 8000

# Start the application with Uvicorn.
# The app object is defined in main.py and exposes FastAPI routes.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
