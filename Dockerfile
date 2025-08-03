# Use Python 3.10 as the base image
FROM python:3.10-slim

# INSTALL MISSING SYSTEM LIBRARIES
# Install all essential libraries required for Qt6
RUN apt-get update && apt-get install -y \
    qt6-base-dev \
    libgl1-mesa-glx \
    libxkbcommon0 \
    libegl1-mesa \
    libdbus-1-3 \
    libfontconfig1 \
    libfreetype6 \
    libglib2.0-0 \
    libxcb-cursor0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Set PYTHONPATH so Python can find modules
ENV PYTHONPATH=/app

# Copy and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Run the main program when container starts
CMD ["python", "main.py"]