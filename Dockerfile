# Χρησιμοποιήστε Python 3.12-slim
FROM python:3.12-slim

# Ορισμός working directory
WORKDIR /app

# Εγκατάσταση απαραίτητων πακέτων για SQLite
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Αντιγραφή όλων των αρχείων
COPY . .

# Εγκατάσταση Python dependencies (με virtual environment)
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Εξαγωγή της θύρας
EXPOSE 5000

# Εκτέλεση της εφαρμογής με virtual environment
CMD ["/venv/bin/python", "app.py"]
