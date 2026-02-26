import os.path
from collections import Counter


def get_slowest_endpoint(file_path, valid_codes):
    with open(file_path, 'r') as file:
        metrics: dict[str, tuple[int, int]] = {}
        for line in file:
            if not line.strip():
                continue

            line_data = line.strip().split(" ")
            try:
                endpoint = line_data[-3]
                http_code = int(line_data[-2])
                response_time = int(line_data[-1][:-2])
            except (IndexError, ValueError):
                continue

            if http_code in valid_codes:
                if endpoint not in metrics:
                    metrics[endpoint] = (0, 0)
                data = metrics[endpoint]
                metrics[endpoint] = (data[0] + response_time, data[1] + 1)

        response_time_by_endpoint = Counter()

        for endpoint, metric in metrics.items():
            response_time_by_endpoint[endpoint] = metric[0] // metric[1]

        return response_time_by_endpoint.most_common(1)


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    log = os.path.join(current_path, "resources/ephemeral_sandboxes.log")
    print(get_slowest_endpoint(log, [200, 201]))
