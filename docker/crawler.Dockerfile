ARG BASE_IMAGE=nvidia/cuda:12.2.0-base-ubuntu22.04
FROM ${BASE_IMAGE}

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    libssl-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libxslt1-dev \
    antiword \
    poppler-utils \
    tesseract-ocr \
    libgl1 \
    chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos '' quantum && \
    chown -R quantum:quantum /app
USER quantum

HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["python", "main.py"]
