FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir grpcio==1.43.0 grpcio-tools==1.43.0 protobuf==3.20.3

EXPOSE 51234

CMD ["python", "banner_service.py"]
