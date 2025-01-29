# Basisimage ist ein Python-Image als Alpine-Version
FROM python:3.13.1-alpine3.20 as backend

EXPOSE 8000

# Arbeitsverzeichnis im Container
WORKDIR /app

# requirements.txt kopieren und installieren
COPY requirements.txt /app
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Code kopieren
COPY /app /app

# Startbefehl
CMD sh -c "python utility_scripts.py && uvicorn main:app --host 0.0.0.0 --port 8000"
