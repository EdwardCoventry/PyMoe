import time
from functools import wraps
from requests import RequestException
import threading

MAX_RETRIES = 5
BASE_WAIT_SECONDS = 2

class RateLimiter:
    def __init__(self, requests_per_minute=60, min_time_between_calls=2.0):
        """
        :param requests_per_minute: Default assumed rate limit from AniList (90).
        :param min_time_between_calls: Additional wait time (in seconds) to prevent bursts.
        """
        self.requests_per_minute = requests_per_minute
        self.remaining_requests = requests_per_minute
        self.reset_time = None

        # The new attributes:
        self.min_time_between_calls = min_time_between_calls
        self._lock = threading.Lock()
        self._last_call_time = 0.0

    def _wait_for_reset(self):
        if self.reset_time:
            now = time.time()
            wait_for_reset_duration = self.reset_time - now
            if wait_for_reset_duration > 0:
                time.sleep(wait_for_reset_duration)
            self.reset_time = None
            self.remaining_requests = self.requests_per_minute

    def _update_rate_limit(self, headers):
        if 'X-RateLimit-Limit' in headers:
            self.requests_per_minute = int(headers['X-RateLimit-Limit'])
        if 'X-RateLimit-Remaining' in headers:
            self.remaining_requests = int(headers['X-RateLimit-Remaining'])

        reset_epoch = headers.get('X-RateLimit-Reset')
        if reset_epoch:
            self.reset_time = int(reset_epoch)

    def _calculate_wait_seconds(self, headers, retries):
        wait_seconds = BASE_WAIT_SECONDS
        retry_after = headers.get('Retry-After')
        if retry_after:
            wait_seconds = int(retry_after)
        wait_seconds += (2 ** retries) * BASE_WAIT_SECONDS
        return max(wait_seconds, 0)  # Ensure waitSeconds is not negative

    def send_request_with_retry(self, request_func, *args, **kwargs):
        retries = 0

        while retries < MAX_RETRIES:
            # 1) Enforce a minimum time between calls (burst limiting)
            with self._lock:
                now = time.time()
                time_since_last = now - self._last_call_time
                if time_since_last < self.min_time_between_calls:
                    time.sleep(self.min_time_between_calls - time_since_last)
                # Update the last call time
                self._last_call_time = time.time()

            # 2) If we have run out of requests, wait for the reset
            if self.remaining_requests <= 0:
                self._wait_for_reset()

            try:
                response, headers = request_func(*args, **kwargs)
                self._update_rate_limit(headers)
                self.remaining_requests -= 1
                return response
            except RequestException as error:
                if error.response and error.response.status_code == 429:
                    wait_seconds = self._calculate_wait_seconds(error.response.headers, retries)
                    time.sleep(wait_seconds)
                    retries += 1
                else:
                    raise

        raise RequestException(
            f"Max retries reached. Rate limit still exceeded after {retries} attempts."
        )

# Create your global instance
rate_limiter = RateLimiter()

def rate_limited(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return rate_limiter.send_request_with_retry(func, *args, **kwargs)
    return wrapper
