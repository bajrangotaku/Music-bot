FROM python:3.11-slim-bullseye

# Install FFmpeg and required packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Working Directory
WORKDIR /app

# Copy Requirements and Install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Run the bot
CMD ["python3", "main.py"]
