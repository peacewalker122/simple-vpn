# Use Ubuntu as the base image
FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install Python and other necessary packages
RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  iproute2 \
  iputils-ping \
  net-tools \
  && rm -rf /var/lib/apt/lists/*

# Copy the Python script into the container
COPY tun.py .

# Run the script when the container launches
CMD ["python3", "tun.py"]
