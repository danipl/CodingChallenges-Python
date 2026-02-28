import time

import httpx


def paginator_with_rate_limiter():
    pr_list = []
    page = 1

    while True:
        try:
            print(f"Fetching page {page}...")
            params = {
                'page': page,
                'per_page': 100
            }
            response = httpx.get(
                'https://api.github.com/repos/kubernetes/kubernetes/pulls',
                params=params
            )
            response.raise_for_status()

            # 1. The Rate Limit Check
            remaining = int(response.headers.get('X-RateLimit-Remaining', 60))
            print(f"Remaining {remaining} RateLimit tokens")
            if remaining < 5:
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time()))
                sleep_duration = max(0, reset_time - int(time.time())) + 1
                print(f"Rate limit critical. Sleeping for {sleep_duration} seconds...")
                time.sleep(sleep_duration)

            # Extract Data
            json_data = response.json()
            for pr in json_data:
                user = pr.get('user') or {}
                pr_list.append({
                    'pr_number': pr.get('number'),
                    'author': user.get('login'),
                    'creation_date': pr.get('created_at')
                })

            # 2. The Header-Driven Pagination
            if 'next' not in response.links:
                break

            page += 1

        except httpx.HTTPError as e:
            print(f"HTTP Error: {e}")
            break

    return pr_list


if __name__ == '__main__':
    prs = paginator_with_rate_limiter()
    print(f"Total PRs fetched: {len(prs)}")
