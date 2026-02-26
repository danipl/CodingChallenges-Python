desired_state = ["sbx-111", "sbx-222", "sbx-333"]
current_state = ["sbx-222", "sbx-333", "sbx-444", "sbx-555"]


def reconcile_sandboxes(desired, current) -> tuple[list[str], list[str]]:
    to_create, to_delete = [], []

    unique_desired_state = set(desired)
    unique_current_state = set(current)

    to_create.extend([candidate for candidate in desired if candidate not in unique_current_state])
    to_delete.extend([candidate for candidate in current if candidate not in unique_desired_state])

    return to_create, to_delete


if __name__ == '__main__':
    print(reconcile_sandboxes(desired_state, current_state))
