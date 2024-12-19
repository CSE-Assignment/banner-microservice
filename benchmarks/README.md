# Benchmarks Directory

This directory contains files and scripts used for benchmarking the performance of the `banner-microservice`.

## Files

- **locustfile.py**  
  Defines Locust tasks to simulate user traffic and test the performance of the `banner-microservice`.  
  Key tasks include simulating gRPC requests to the `GetCurrentBanner` endpoint.

- **validate_benchmark.py**  
  A Python script that validates the benchmarking results against predefined performance thresholds (e.g., response time, failure rate). It ensures the service meets the required performance standards.

## Running Benchmarks

To run benchmarks and generate performance reports, follow these steps:

1. **Start the Service**  
   Ensure the `banner-microservice` is running and accessible at the correct host and port (default: `http://127.0.0.1:51234`).

2. **Run Locust**  
   Execute the following command to simulate traffic using Locust:
   ```bash
   locust -f benchmarks/locustfile.py --headless -u 100 -r 10 --run-time 1m --host http://127.0.0.1:51234 --csv locust_logs
   ```
   - `-u 100`: Simulates 100 users.
   - `-r 10`: Spawns 10 users per second.
   - `--run-time 1m`: Runs the test for 1 minute.
   - `--csv locust_logs`: Outputs results to CSV files in the `locust_logs/` directory.
   
3. **Validate Benchmark Results**  
   After the benchmark run, validate the results by running:
   ```bash
   python benchmarks/validate_benchmark.py
   ```
   This script checks if the performance metrics meet predefined thresholds. If any thresholds are exceeded, it will log an error.
   
## Benchmark Output

Benchmarking results will be stored as CSV files in the `locust_logs/` directory. Key files include:

- **locust_logs_stats.csv**: Summary of performance metrics.
- **locust_logs_stats_failures.csv**: List of failed requests.
- **locust_logs_stats_exceptions.csv**: Detailed exception logs.
- **locust_logs_stats_stats_history.csv**: Historical performance data over the run.

