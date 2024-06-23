# Use the official Python slim image
FROM python:3.10.12-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .


# Install the required Python packages
RUN pip install --no-cache-dir --upgrade pip

# Debugging step: Capture and output logs of pip install
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run the application
CMD ["python3", "polybot/bot.py"]

EXPOSE 5000
