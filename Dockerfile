FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# System dependencies (WeasyPrint, Pillow, Tesseract and related libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libxml2-dev libxslt1-dev libffi-dev \
    libjpeg-dev zlib1g-dev \
    tesseract-ocr \
    poppler-utils \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    shared-mime-info \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install -r /app/requirements.txt

# Copy application
COPY . /app

# Default port used by Render. Keep fallback to 5000 for local runs.
ENV PORT=5000
EXPOSE 5000

# Use gunicorn to run the app. Use shell form so $PORT expands.
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "run:app"]
