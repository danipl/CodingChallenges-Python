import os
from collections import Counter


def get_top_500_errors(file_path):
    # Counter is a dictionary specifically designed for tallying
    error_counts = Counter()

    # 1. 'with' ensures the file descriptor is closed safely
    # 2. Iterating directly over 'file' saves RAM
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines
            if not line.strip():
                continue

            # split() with no arguments splits by any whitespace safely
            values = line.split()
            ip = values[0]
            status_code = values[-2]

            # 3. Filter for exactly what we care about
            if status_code == "500":
                error_counts[ip] += 1

    # 4. Counter has a built-in method to sort and return the top N results
    return error_counts.most_common(2)


script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "resources/raw_nginx.log")

print(get_top_500_errors(log_path))
