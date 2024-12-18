import csv
import sys
import os

def validate_benchmark_results(csv_file, thresholds):
    """
    Validates benchmark results against predefined thresholds.

    Args:
        csv_file (str): Path to the Locust CSV file (e.g., summary stats).
        thresholds (dict): Thresholds for metrics.

    Raises:
        ValueError: If any metric fails to meet its threshold.
    """
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' does not exist.")
        sys.exit(1)

    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        if not rows:
            print("Error: CSV file is empty.")
            sys.exit(1)

        # Use the last row of CSV as the summary stats
        stats = rows[-1]

        # Validate metrics
        errors = []
        for metric, threshold in thresholds.items():
            if metric not in stats:
                errors.append(f"Metric '{metric}' not found in CSV.")
                continue

            try:
                metric_value = float(stats[metric])
                if metric_value > threshold:
                    errors.append(f"Threshold exceeded for {metric}: {metric_value} > {threshold}")
            except ValueError:
                errors.append(f"Invalid value for metric '{metric}': {stats[metric]}")

        if errors:
            print("Benchmark validation failed:")
            for error in errors:
                print(f" - {error}")
            sys.exit(1)
        
        print("All metrics passed threshold checks!")
    except Exception as e:
        print(f"Error validating benchmarks: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Define performance thresholds
    THRESHOLDS = {
        "Average Response Time": 1000,  # Max average response time in ms
        "Failure Rate": 1.0,           # Max failure rate in %
        "Requests/s": 50               # Min requests per second
    }

    # Path to the Locust CSV summary file
    CSV_FILE = "locust_logs_stats.csv" 

    validate_benchmark_results(CSV_FILE, THRESHOLDS)
