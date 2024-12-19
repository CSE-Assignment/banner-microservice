# Banner Microservice

The **Banner Microservice** is a gRPC-based service for delivering dynamic banner content based on user location and time. This repository includes source code, testing, benchmarking, and deployment instructions to ensure seamless development and integration.

## Core Features
- **Dynamic Banner Delivery**: Serve customized banners based on user location and time.
- **Performance Benchmarking**: Evaluate service performance under load with Locust.
- **Comprehensive Testing**: Includes unit, component, and end-to-end tests.

## Directory Overview

### `tests/`
Contains test files to ensure the reliability of the microservice.
- **Run Unit Tests**: `pytest -m unit tests/`
- **Run Component Tests**: `pytest -m component tests/`
- **Run End-to-End Tests**: Start the service and execute: `pytest -m e2e tests/`

### `benchmarks/`
Includes benchmarking tools and validation scripts.
**Run Benchmarks**: Simulate traffic using Locust.
  ```bash
  locust -f benchmarks/locustfile.py --headless -u 100 -r 10 --run-time 1m --host http://127.0.0.1:51234 --csv locust_logs
  ```
- `-u 100`: Simulates 100 users.
- `-r 10`: Spawns 10 users per second.
- `--run-time 1m`: Runs the test for 1 minute.
- `--csv locust_logs`: Outputs results to CSV files in the `locust_logs/` directory.
 
## Benchmark Output

Benchmarking results will be stored as CSV files in the `locust_logs/` directory. Key files include:

- **locust_logs_stats.csv**: Summary metrics.
- **locust_logs_stats_failures.csv**: Failed requests.
- **locust_logs_stats_exceptions.csv**: Exception logs.
- **locust_logs_stats_stats_history.csv**: Historical data.


## `.github/workflows/`

Automates testing and benchmarking workflows using GitHub Actions.

### 1. Automated Testing:
- Triggers on every pull request or push to the main branch.
- Runs unit, component, and end-to-end tests.
### 2. Benchmarking:
- Triggers on-demand or weekly via workflow_dispatch.
- Executes Locust tests and validates performance thresholds.


# Getting Started

## Prerequisites 

- Python 3.12+
- Docker (for containerized environments)

