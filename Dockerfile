# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1-mesa-glx \
    curl \
    python-dotenv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Snyk
RUN curl -Lo snyk https://github.com/snyk/snyk/releases/latest/download/snyk-linux \
    && chmod +x snyk \
    && mv snyk /usr/local/bin/

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the working directory to the polybot directory
WORKDIR /app/polybot

# Expose port 5000
EXPOSE 5000

# Run the bot when the container launches
CMD ["python3", "bot.py"]
