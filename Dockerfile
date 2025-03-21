# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install sqlite3
RUN apt update && apt install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Default command for the container
CMD ["python", "app.py"]
