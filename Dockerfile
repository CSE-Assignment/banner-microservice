FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install --upgrade protobuf==3.20.3
RUN pip install --no-cache-dir grpcio grpcio-tools

EXPOSE 51234

CMD ["python", "banner_service.py"]
