import json
import os.path


def sandbox_abandoned_cost_per_hour(file_path, status="abandoned"):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    total_cost = 0.0
    for sandbox in json_data.get("data", []):
        if sandbox.get("status") == status:
            total_cost += sandbox.get("cost_per_hour", 0.0)

    return total_cost


if __name__ == "__main__":
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_name, "./resources/internal_sandboxes_request.json")
    print(f"Total cost per hour of abandoned sandboxes: {sandbox_abandoned_cost_per_hour(file_path)}")
