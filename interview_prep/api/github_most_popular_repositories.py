from collections import Counter

import requests

HEADERS = {
    'Accept': 'application/vnd.github.v3+json'
}


def get_top_hashicorp_repos():
    repositories = []
    page = 1
    while True:
        try:
            params = {
                'page': page,
                'per_page': 100,
                'sort': 'updated',
                'direction': 'desc'
            }
            response = requests.get('https://api.github.com/orgs/hashicorp/repos', params=params, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            repositories.extend(
                (repo.get('name'), int(repo.get('stargazers_count', 0))) for repo in data if repo.get('name')
            )
            if len(data) < 100:
                break
            page += 1
        except requests.exceptions.RequestException as re:
            print(f"HTTP API request failed: {re}")
            break

    starts_counter = Counter()

    for repo in repositories:
        starts_counter[repo[0]] = repo[1]

    return starts_counter.most_common(3)


if __name__ == '__main__':
    print(get_top_hashicorp_repos())
