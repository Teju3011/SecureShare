import pytest
from app.core.rate_limit import InMemoryRateLimiter


def test_rate_limiter_logic():
    limiter = InMemoryRateLimiter()
    key = "test_client_ip:127.0.0.1"

    # Allow up to 5 requests
    for _ in range(5):
        limited, _ = limiter.is_rate_limited(key, max_requests=5, window_seconds=60)
        assert limited is False

    # 6th request is blocked
    limited, retry_after = limiter.is_rate_limited(key, max_requests=5, window_seconds=60)
    assert limited is True
    assert retry_after > 0
