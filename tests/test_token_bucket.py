import pytest
from fastapi import HTTPException
from app.rate_limiter import check_token_bucket_limit, TOKEN_BUCKETS, TOKEN_BUCKET_CONFIG
import time


def reset_buckets():
    for key in TOKEN_BUCKETS:
        TOKEN_BUCKETS[key]['tokens'] = TOKEN_BUCKET_CONFIG[key]['capacity']
        TOKEN_BUCKETS[key]['last_refill'] = time.time()


def test_user_token_bucket_limit():
    reset_buckets()
    role = "user"
    # user capacity = 5
    for _ in range(5):
        check_token_bucket_limit(role)  # should pass

    with pytest.raises(HTTPException) as excinfo:
        check_token_bucket_limit(role)
    assert "Token bucket rate limit exceeded" in str(excinfo.value)


def test_admin_unlimited_bucket():
    role = "admin"
    # should never raise
    for _ in range(20):
        check_token_bucket_limit(role)


def test_bucket_refill():
    reset_buckets()
    role = "user"
    for _ in range(5):
        check_token_bucket_limit(role)
    # now bucket empty
    time.sleep(12)  # token bucket adds 1 token per ~12 sec
    check_token_bucket_limit(role)  # should succeed now
