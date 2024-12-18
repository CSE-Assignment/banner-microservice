import json
import sys

def validate_benchmark_results(csv_file, thresholds):
    """
    Validates benchmark results against predefined thresholds.

    Args:
        csv_file (str): Path to the Locust CSV file (e.g., summary stats).
        thresholds (dict): Thresholds for metrics.

    Raises:
        ValueError: If any metric fails to meet its threshold.
    """
    try:
        with open(csv_file, 'r') as file:
            lines = file.readlines()

        # Parse last line of CSV (summary stats)
        headers = lines[0].strip().split(',')
        values = lines[-1].strip().split(',')
        stats = dict(zip(headers, values))

        # Validate metrics
        for metric, threshold in thresholds.items():
            if float(stats[metric]) > threshold:
                print(f"Threshold exceeded for {metric}: {stats[metric]} > {threshold}")
                raise ValueError(f"Performance validation failed for {metric}")
        
        print("All metrics passed threshold checks!")
    except Exception as e:
        print(f"Error validating benchmarks: {e}")
        sys.exit(1)

if __name__ == "__main__":
    THRESHOLDS = {
        "response_time": 1000,  # Max response time in ms
        "failure_rate": 1,     # Max failure rate in %
    }
    CSV_FILE = "locust_logs_stats.csv"  # Update with your CSV file path
    validate_benchmark_results(CSV_FILE, THRESHOLDS)
