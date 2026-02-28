import httpx


def reconcile_labels(repo_owner, repo_name, desired_labels, github_token=None):
    present = set()
    try:
        headers = {'Authorization': f"Bearer {github_token}"} if github_token else {}
        page = 1
        while True:
            params = {
                'page': page,
                'per_page': 100,
                'sort': 'updated',
                'direction': 'desc'
            }
            response = httpx.get(
                f"https://api.github.com/repos/{repo_owner}/{repo_name}/labels",
                params=params,
                headers=headers
            )
            response.raise_for_status()
            json_data = response.json()
            present.update(set([label.get('name') for label in json_data if label.get('name')]))
            if len(json_data) < 100:
                break
            page += 1
    except httpx.HTTPError as e:
        print(f"Error requesting labels from {repo_owner}/{repo_name}")
        raise e

    desired = set(desired_labels)
    to_create = desired - present
    to_delete = present - desired

    return to_create, to_delete


if __name__ == '__main__':
    to_create, to_delete = reconcile_labels(
        'kubernetes',
        'kubernetes',
        ['create_1', 'create_2', 'area/admin', 'area/build-release', 'area/cadvisor']
    )
    print(f"To create: {to_create}")
    print(f"To delete: {to_delete}")
