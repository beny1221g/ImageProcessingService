# Use the official Python slim image
FROM python:3.10.12-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN sudo pip install --no-cache-dir --upgrade pip
RUN sudo pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .
RUN cd polybot
# Specify the command to run the application
CMD ["python3", "bot.py"]

EXPOSE 5000
