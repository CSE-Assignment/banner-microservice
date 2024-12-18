import sys
import os

def validate_benchmark_results(csv_file, thresholds):
    """
    Validates benchmark results against predefined thresholds.

    Args:
        csv_file (str): Path to the Locust stats CSV file.
        thresholds (dict): Thresholds for metrics.

    Raises:
        ValueError: If any metric fails to meet its threshold.
    """
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' does not exist.")
        sys.exit(1)

    try:
        with open(csv_file, 'r') as file:
            lines = file.readlines()

        headers = lines[0].strip().split(',')
        values = lines[-1].strip().split(',')
        stats = dict(zip(headers, values))

        for metric, threshold in thresholds.items():
            if float(stats.get(metric, 0)) > threshold:
                print(f"Threshold exceeded for {metric}: {stats[metric]} > {threshold}")
                raise ValueError(f"Performance validation failed for {metric}")
        
        print("All metrics passed threshold checks!")
    except Exception as e:
        print(f"Error validating benchmarks: {e}")
        sys.exit(1)

if __name__ == "__main__":
    THRESHOLDS = {
        "Avg Response Time": 1000,  # Max average response time in ms
        "Failure Count": 1,        # Max number of failures
    }
    CSV_FILE = "locust_logs_stats_stats.csv"
    validate_benchmark_results(CSV_FILE, THRESHOLDS)
