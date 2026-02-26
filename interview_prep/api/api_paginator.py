import json
import os.path

import requests


def fetch_page(url, page_number) -> dict:
    try:
        response = requests.get(url, timeout=30, params={'page_number': page_number})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call error: {e}")
        dir_name = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_name, f"./resources/{page_number}_api_paginator_request.json")
        if os.path.exists(file_path):
            with open(file_path) as file:
                return json.load(file)
        else:
            return {}


def get_all_sandbox_ids(base_url):
    page = 0
    sandbox_ids = []
    while page is not None:
        json_response = fetch_page(base_url, page)
        next_page_value = json_response.get('next_page', None)
        page = int(next_page_value) if next_page_value else None
        sandbox_ids.extend([s.get('id') for s in json_response.get('data', []) if s.get('id')])

    return sandbox_ids


if __name__ == '__main__':
    print(get_all_sandbox_ids('https://api.deel.internal/sandboxes'))
