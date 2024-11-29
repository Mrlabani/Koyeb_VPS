# Start with an Ubuntu base image
FROM ubuntu:20.04

# Set the working directory
WORKDIR /app

# Set DEBIAN_FRONTEND to noninteractive to avoid tzdata prompt
ENV DEBIAN_FRONTEND=noninteractive

# Pre-configure tzdata to avoid interactive prompt
RUN echo "tzdata tzdata/Areas select Etc" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/Etc select UTC" | debconf-set-selections

# Install required packages and Python 3.10
RUN apt update && apt install -y \
    software-properties-common \
    curl \
    bash \
    bzip2 \
    git \
    neofetch \
    wget \
    sudo \
    xvfb \
    unzip \
    ffmpeg && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-distutils \
    python3-pip && \
    apt-get clean

# Set Python 3.10 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install html5lib explicitly (as pip might need it)
RUN python3 -m pip install html5lib

# Upgrade pip to the latest version to avoid internal issues
RUN python3 -m pip install --upgrade pip

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN python3 -m pip install -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Set the default command to run the application
CMD ["python3", "vps.py"]