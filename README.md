# Banner Microservice

The **Banner Microservice** is a gRPC-based service for delivering dynamic banner content based on user location and time. This repository includes source code, testing, benchmarking, and deployment instructions to ensure seamless development and integration.

# More Docs

1. README in `tests/`
2. README in `benchmarks/`
3. README in `.github/workflows/`

## Core Features
- **Dynamic Banner Delivery**: Serve customized banners based on user location and time.
- **gRPC API**: Efficient communication with other microservices.
- **Configuration-Driven**: Easily manage banners via JSON files.
- **Kubernetes Deployment**: Fully containerized and deployable with Skaffold.
- **Performance Benchmarking**: Evaluate service performance under load with Locust.
- **Comprehensive Testing**: Includes unit, component, and end-to-end tests.

# Getting Started

## Quick Start Guide - Banner Feature

To test the promotional banner feature you need to start our fork of the Google Microservices Demo. Following are the steps.

### Prerequisites
- Python 3.12+
- Docker
- Skaffold
- Minikube

### Steps
1. Clone the Microservices Demo fork repository and the Banner Service submodule:
   ```
   git clone --recurse-submodules https://github.com/CSE-Assignment/microservices-demo.git
   cd microservices-demo
   ```
2. Assuming docker is running, start minikube (ensure minikube has at least 4 CPUs, 4.0 GiB memory, 32 GB disk space):
   ```
   minikube start
   ```
3. Run `kubectl get nodes` to verify you're connected to the respective control plane.
4. Run `skaffold run` (first time will be slow, it can take ~20 minutes). This will build and deploy the application.
5. Run `kubectl get pods` to verify the Pods are ready and running.
6. Run `kubectl port-forward deployment/frontend 8080:8080` to forward a port to the frontend service.
7. Navigate to `localhost:8080` to access the web frontend.
8. Use the country dropdown in the navigation bar to display different banners based on location.
9. Select `GB` as the location. Every odd minute a `Flash Sale Coming Soon` banner will be displayed, every even minute a `Flash Sale` banner will be displayed, for showcasing time-based selection.

## Quick Start Guide - Testing/Benchmarking

To try out the testing/benchmarking capabilities of this project refer to the README in `./tests` and `./benchmarks`.

# Technical Documentation

## gRPC API Specification

### GetCurrentBanner
- **Endpoint**: `BannerService.GetCurrentBanner`
- **Request**:
  ```
  {
    "location": "string"
  }
  ```
- **Response**:
  ```
  {
    "title": "string",
    "description": "string",
    "image": "bytes",
    "image_format": "string"
  }
  ```

## Configuration
Banner configurations are stored in JSON files in `resources/configs/`. Example configuration:
```
{
  "id": "example",
  "title": "Holiday Sale",
  "description": "50% off on selected items!",
  "start_time": "2024-12-01T00:00:00Z",
  "end_time": "2024-12-25T23:59:59Z",
  "locations": ["US", "CA"]
}
```

# QA - Directory Overview

## Testing Overview

To try out the testing capabilities and read more documentation on testing refer to the README in `./tests`.

`tests/` Contains test files to ensure the reliability of the microservice.
- **Run Unit Tests**: `pytest -m unit tests/`
- **Run Component Tests**: `pytest -m component tests/`
- **Run End-to-End Tests**: Start the service and execute: `pytest -m e2e tests/`

## Benchmarking

`benchmarks/` Includes benchmarking tools and validation scripts.
**Run Benchmarks**: Simulate traffic using Locust.
  ```bash
  locust -f benchmarks/locustfile.py --headless -u 100 -r 10 --run-time 1m --host http://127.0.0.1:51234 --csv locust_logs
  ```
- `-u 100`: Simulates 100 users.
- `-r 10`: Spawns 10 users per second.
- `--run-time 1m`: Runs the test for 1 minute.
- `--csv locust_logs`: Outputs results to CSV files in the `locust_logs/` directory.
 
### Benchmark Output

Benchmarking results will be stored as CSV files in the `locust_logs/` directory. Key files include:

- **locust_logs_stats.csv**: Summary metrics.
- **locust_logs_stats_failures.csv**: Failed requests.
- **locust_logs_stats_exceptions.csv**: Exception logs.
- **locust_logs_stats_stats_history.csv**: Historical data.


## Workflows

`.github/workflows/` Automates testing and benchmarking workflows using GitHub Actions.

### 1. Automated Testing:
- Triggers on every pull request or push to the main branch.
- Runs unit, component, and end-to-end tests.
### 2. Benchmarking:
- Triggers on-demand or weekly via workflow_dispatch.
- Executes Locust tests and validates performance thresholds.
