# Use an official Python runtime as a parent image
FROM python:3.13.0b2-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm (if not already included in base image)
# Example if you decide to use Node.js and npm
# RUN apt-get install -y nodejs npm

# Set the working directory in the container
WORKDIR /app

# Install snyk globally using npm
RUN npm install -g snyk

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the working directory to the polybot directory
WORKDIR /app/polybot

# Run the bot when the container launches
CMD ["python3", "bot.py"]

# Expose port 5000 (if necessary)
EXPOSE 5000
