import os
import time
from collections import defaultdict
from threading import Lock
from typing import Dict, List, Tuple
from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    def __init__(self):
        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._lock = Lock()

    def is_rate_limited(self, key: str, max_requests: int, window_seconds: int) -> Tuple[bool, int]:
        now = time.time()
        window_start = now - window_seconds
        with self._lock:
            # Purge expired timestamps
            self._requests[key] = [t for t in self._requests[key] if t > window_start]
            count = len(self._requests[key])
            if count >= max_requests:
                oldest = self._requests[key][0]
                retry_after = max(1, int(oldest + window_seconds - now))
                return True, retry_after
            self._requests[key].append(now)
            return False, 0

    def reset(self):
        with self._lock:
            self._requests.clear()


limiter = InMemoryRateLimiter()


def rate_limit_check(key_prefix: str, max_requests: int = 30, window_seconds: int = 60):
    async def dependency(request: Request):
        if os.getenv("ENVIRONMENT") == "testing" and os.getenv("ENABLE_TEST_RATE_LIMIT") != "true":
            return
        client_ip = request.client.host if request.client else "unknown"
        key = f"{key_prefix}:{client_ip}"
        limited, retry_after = limiter.is_rate_limited(key, max_requests, window_seconds)
        if limited:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many requests. Please retry after {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)}
            )
    return dependency
