FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Set production environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Install Python dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt && \
    ln -s /venv/bin/pytest /usr/local/bin/pytest

# Run tests
RUN /venv/bin/pip install --no-cache-dir pytest
RUN /venv/bin/pytest

# Create the data directory for the database
RUN mkdir -p /app/data

EXPOSE 5000

CMD ["/venv/bin/python", "app.py"]
