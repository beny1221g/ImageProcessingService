# Use an official Python runtime as a parent image
FROM python:3.13.0b2-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

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

# Expose port 5000
EXPOSE 5000

#CMD "python3 -m polybot.bot"
