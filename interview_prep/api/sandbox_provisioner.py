import json
import os.path

import requests


def get_prs_for_sandboxes(api_url, fallback_json_data=None) -> list[int]:
    try:
        response = requests.get(api_url, timeout=30, headers={"Authorization": "Bearer ..."})
        response.raise_for_status()  # Throws an exception if status is 4xx or 5xx
        payload = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error occurred: {e}")
        if fallback_json_data:
            with open(fallback_json_data, 'r') as file:
                payload = json.load(file)
        else:
            return []

    if not payload:
        return []

    pr_ids = []

    for pr in payload:
        if pr.get('state') == 'open' and 'needs-sandbox' in pr.get('labels', []):
            pr_id = pr.get('id')
            if pr_id:
                pr_ids.append(pr_id)

    return pr_ids


if __name__ == '__main__':
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_name, './resources/sandbox_provisioner_request.json')
    print(get_prs_for_sandboxes('https://api.github.internal/v1/pulls', file_path))
