import json
import os.path
from collections import Counter

import httpx


def get_top_failing_stage(url, fallback_source):
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        pipelines = response.json()
    except httpx.HTTPError as e:
        print(f"HTTP request failed, use fallback: {e}")
        dir_name = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_name, fallback_source)
        with open(file_path, 'r') as file:
            pipelines = json.load(file)

    endpoint_counter = Counter()

    for pipeline in pipelines:
        status = pipeline.get('status', '')
        failed_stage = pipeline.get('failed_stage')
        if status == 'failed' and failed_stage:
            endpoint_counter[failed_stage] += 1

    return endpoint_counter.most_common(1)


if __name__ == '__main__':
    print(get_top_failing_stage(
        'https://api.deel.internal/v1/pipelines/recent',
        './resources/pipelines_info_request.json'
    ))
