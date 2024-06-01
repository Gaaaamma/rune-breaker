# Use the official Python 3.8 image from the Docker Hub
FROM python:3.8-slim

# Set environment variables for timezone and non-interactive frontend
ENV TZ=Asia/Taipei
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install tzdata for setting the timezone
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run your application
CMD ["python", "-m", "main"]