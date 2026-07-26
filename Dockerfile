FROM python:3.11-slim-bullseye

# Install FFmpeg and required build tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    gcc \
    python3-dev \
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
