# Tests Directory

This directory contains all the test cases for the `banner-microservice` project. The tests are organized into different categories to ensure comprehensive coverage for unit, component, and end-to-end testing.

## Test Files

### 1. **`test_banner_config.py`**
- **Purpose:** Validates the functionality of `banner_config.py`, including banner configuration loading and validation.
- **Type:** Unit Test
- **Scope:**
  - Test banner configuration files.
  - Validate datetime parsing and format compliance.
  - Ensure missing or invalid fields are handled correctly.

### 2. **`test_banner_service.py`**
- **Purpose:** Unit tests for the core logic of the `banner_service.py` file.
- **Type:** Unit Test
- **Scope:**
  - Test the `GetCurrentBanner` gRPC method.
  - Validate responses for valid and invalid banner requests.
  - Ensure appropriate error handling and fallback to default banners.

### 3. **`test_banner_service_component.py`**
- **Purpose:** Component tests for the `banner_service.py`, focusing on its interaction with external components and dependencies.
- **Type:** Component Test
- **Scope:**
  - Validate integration between `banner_service.py` and the banner configuration loader.
  - Test system behavior with mock dependencies to simulate real-world scenarios.

### 4. **`test_banner_service_e2e.py`**
- **Purpose:** End-to-end testing for the `banner_service.py` when deployed as a complete microservice.
- **Type:** End-to-End Test
- **Scope:**
  - Simulate real-world gRPC client-server interactions.
  - Validate that the service returns the expected banner data for various inputs.
  - Ensure the service is functional in a live environment.

---

## Running Tests

**Setup:**
Ensure all dependencies are installed:
```bash
python -m pip install -r requirements.txt
```

### Run Unit Tests
Execute the following command to run all unit tests:
```bash
pytest -m unit tests/
```
### Run Component Tests
Execute the following command to run all component tests:
```bash
pytest -m component tests/
```
### Run End-to-End Tests
Ensure the service is running before executing end-to-end tests:
```bash
pytest -m e2e tests/
```
