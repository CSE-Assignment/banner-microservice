# GitHub Workflows

This directory contains the GitHub Actions workflows for the **banner-microservice** project. These workflows automate various tasks like testing, benchmarking, and other CI/CD processes.

## Workflows

### 1. `automated-testing.yml`
- **Purpose**: Runs automated unit, component, and end-to-end tests for the banner microservice.
- **Trigger**: Executes on every pull request or push to the main branch.
- **Details**:
  - Sets up the Python environment.
  - Installs required dependencies.
  - Executes different types of tests with `pytest`.
  - Uploads test results as artifacts.

### 2. `benchmark.yml`
- **Purpose**: Performs benchmarking on the banner microservice to evaluate its performance under load.
- **Trigger**:
  - Can be manually triggered using `workflow_dispatch`.
  - Scheduled to run every Sunday at 2 AM.
- **Details**:
  - Sets up Python and installs Locust for load testing.
  - Executes Locust tests to simulate traffic to the service.
  - Validates the results against predefined thresholds using `validate_benchmark.py`.
  - Uploads benchmark results as artifacts for further analysis.

These workflows streamline development and ensure the service remains performant and reliable.

