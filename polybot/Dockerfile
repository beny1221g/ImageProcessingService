# Install system dependencies and build tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgl1-mesa-glx \
        npm \
        zlib1g-dev \
        build-essential \
        python3-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Install Snyk globally using npm
RUN npm install -g snyk

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY .env .env

# Copy the rest of the application code
COPY . .


# Ensure the directory structure is correct
RUN ls -la /app

# Set the working directory to /app
WORKDIR /app

# Expose port 5000
EXPOSE 5000

# Command to run the bot when the container launches
CMD ["python3", "-m", "polybot.bot"]
