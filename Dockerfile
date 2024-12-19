FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir grpcio grpcio-tools locust

EXPOSE 51234

CMD ["bash", "-c", "python banner_service.py & sleep 10 && locust -f benchmarks/locustfile.py --headless -u 100 -r 10 --run-time 1m --host http://127.0.0.1:51234 --csv=locust_logs/locust_logs_stats"]

ENV PYTHONPATH=/app:/app/generated
