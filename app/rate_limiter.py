# app/rate_limiter.py

import time
from fastapi import HTTPException

# ===============================
# SLIDING WINDOW IMPLEMENTATION
# ===============================

REQUEST_LOG = {}
WINDOW_SIZE = 60  # seconds

SLIDING_LIMITS = {
    "admin": None,
    "user": 5,
    "guest": 0
}


def check_sliding_window_limit(role: str):
    limit = SLIDING_LIMITS.get(role, 0)

    if limit is None:
        return

    now = time.time()
    window_start = now - WINDOW_SIZE

    if role not in REQUEST_LOG:
        REQUEST_LOG[role] = []

    # Remove old timestamps
    REQUEST_LOG[role] = [
        ts for ts in REQUEST_LOG[role]
        if ts > window_start
    ]

    if len(REQUEST_LOG[role]) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Sliding window rate limit exceeded"
        )

    REQUEST_LOG[role].append(now)


# ===============================
# TOKEN BUCKET IMPLEMENTATION
# ===============================

TOKEN_BUCKETS = {}

TOKEN_BUCKET_CONFIG = {
    "admin": {
        "capacity": None,  # unlimited
        "refill_rate": None
    },
    "user": {
        "capacity": 5,      # max burst
        "refill_rate": 5/60  # 5 tokens per minute
    },
    "guest": {
        "capacity": 0,
        "refill_rate": 0
    }
}


def check_token_bucket_limit(role: str):
    config = TOKEN_BUCKET_CONFIG.get(role)

    if not config:
        raise HTTPException(status_code=429, detail="No rate config")

    # Unlimited role
    if config["capacity"] is None:
        return

    now = time.time()

    if role not in TOKEN_BUCKETS:
        TOKEN_BUCKETS[role] = {
            "tokens": config["capacity"],
            "last_refill": now
        }

    bucket = TOKEN_BUCKETS[role]

    # Calculate elapsed time
    elapsed = now - bucket["last_refill"]

    # Refill tokens
    refill_amount = elapsed * config["refill_rate"]
    bucket["tokens"] = min(
        config["capacity"],
        bucket["tokens"] + refill_amount
    )

    bucket["last_refill"] = now

    if bucket["tokens"] < 1:
        raise HTTPException(
            status_code=429,
            detail="Token bucket rate limit exceeded"
        )

    bucket["tokens"] -= 1
