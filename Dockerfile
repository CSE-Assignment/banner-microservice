FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libssl-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
       grpcio==1.43.0 \
       grpcio-tools==1.43.0 \
       protobuf==3.20.3 \
       pytest==7.2.1 \
       pytest-mock==3.10.0

COPY . .

EXPOSE 51234

CMD ["python", "banner_service.py"]
