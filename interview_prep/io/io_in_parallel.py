import asyncio
import random
import time

import httpx


async def io_task(name, min_time, max_time):
    print(f"[{name}] Starting...")

    last_time = random.randint(min_time, max_time)
    await asyncio.sleep(last_time)

    request_time = time.time()
    response = httpx.get("http://www.google.com")
    request_time = time.time() - request_time

    print(f"[{name}] Released.")

    return f"[{name}] lasts {(request_time * 100):.2f}ms with {response.status_code}"


async def run_task():
    futures = {io_task(f"name_{item}", 2, 10): f"name_{item}" for item in range(20)}
    result = await asyncio.gather(*futures)
    print("")
    for line in result:
        print(line)


if __name__ == '__main__':
    asyncio.run(run_task())
