# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt update && apt install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copy the application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
