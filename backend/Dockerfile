# Basisimage ist ein Python-Image als Alpine-Version
FROM python:3.13.1-alpine3.20 as backend
COPY ./backend/ /backend/

# Arbeitsverzeichnis im Container
WORKDIR /app

# requirements.txt kopieren und installieren
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Code kopieren
COPY . /app

# Startbefehl
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

