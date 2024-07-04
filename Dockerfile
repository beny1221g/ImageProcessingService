# Use an official Python runtime as a parent image
FROM python:3.10.12-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    python3-venv \
    snyk\
    && rm -rf /var/lib/apt/lists/*

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

# Expose port 5000
EXPOSE 5000

#CMD "python3 -m polybot.bot"
