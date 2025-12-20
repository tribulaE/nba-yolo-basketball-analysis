FROM python:3.11-slim

WORKDIR /app

RUN apt-get update -o Acquire::Retries=5 && apt-get install -y --no-install-recommends \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*



RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV YOLO_CONFIG_DIR=/tmp/ultralytics
CMD ["python", "-m", "nba_analysis.main"]
