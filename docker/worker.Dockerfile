FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker.py .
COPY crawler/ ./crawler/
COPY utils/ ./utils/

CMD ["python", "worker.py", "-r", "crawler"]
