import random
import time
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor


def io_task(name, min_time, max_time):
    print(f"[{name}] Starting...")

    last_time = random.randint(min_time, max_time)
    time.sleep(last_time)

    print(f"[{name}] Released.")

    return last_time


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(io_task, f"name_{item}", 2, 10): f"name_{item}" for item in range(20)}
        result = []
        for future in as_completed(futures):
            task_name = futures[future]
            try:
                result.append(f"[{task_name}] lasts {future.result(timeout=30)}")
            except TimeoutError as te:
                print(f"{task_name} failed: {te}")
    print("")
    for line in result:
        print(line)