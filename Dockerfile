# Use Python 3.10.8 image
FROM python:3.10.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory content into the container
COPY . /app

# Install basic required packages
RUN apt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run the python script 'vps.py'
CMD ["python", "vps.py"]