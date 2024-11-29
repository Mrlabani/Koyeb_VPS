# Use a lightweight version of Ubuntu as the base image
FROM ubuntu:20.04


# Set environment variables to ensure that the installation runs without user interaction
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.10, pip, and basic dependencies
RUN apt update && apt install -y \
    software-properties-common \
    bash \
    bzip2 \
    git \
    neofetch \
    wget \
    sudo \
    xvfb \
    unzip \
    ffmpeg

RUN apt-get update && \
    apt-get install -y \
    python3.10 \
    python3.10-distutils \
    python3-pip \
    curl \
    build-essential \
    && apt-get clean

# Install necessary Python packages using pip
RUN python3.10 -m pip install --upgrade pip

# Copy the requirements.txt file into the Docker image
COPY requirements.txt /app/requirements.txt

# Install the Python dependencies from the requirements.txt file
RUN python3.10 -m pip install -r /app/requirements.txt

# Copy your bot script into the Docker image
COPY bot.py /app/bot.py

# Expose port 8000 for the bot (if needed for communication)
EXPOSE 8000

# Set the working directory to /app
WORKDIR /app

# Run the bot when the container starts
CMD ["python3.10", "vps.py"]