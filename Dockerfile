FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir grpcio grpcio-tools
RUN pip install --upgrade protobuf==3.20.3

EXPOSE 51234

CMD ["python", "banner_service.py"]
