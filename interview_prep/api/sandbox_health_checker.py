import concurrent.futures
import requests

urls = [
    "http://sandbox-1.deel.internal/healthz",
    "http://sandbox-2.deel.internal/healthz"
]

def check_health(url):
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def check_all_sandboxes(url_list):
    # Dictionary to hold our final mapping of URL -> Status
    health_results = {}

    # 1. The context manager spins up the threads and tears them down safely
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

        # 2. Map each Future back to its original URL so we know which one finished
        # Notice: check_health has no parentheses here!
        future_to_url = {executor.submit(check_health, url): url for url in url_list}

        # 3. as_completed yields the futures the moment their background thread finishes
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                # .result() extracts the actual True/False from the background thread
                status = future.result()
                health_results[url] = status
            except Exception:
                # Catch any unexpected thread crashes
                health_results[url] = False

    return health_results

if __name__ == '__main__':
    print(check_all_sandboxes(urls))