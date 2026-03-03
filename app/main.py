# app/main.py

from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, Depends
from app.llm_client import query_llm
from app.validators import validate_prompt
from app.auth import verify_api_key, authorize
from app.rate_limiter import check_token_bucket_limit
from app.exceptions import ValidationError, LLMGatewayError
from app.logger import log_event
import logging
import time

# Load environment variables
load_dotenv()
API_GATEWAY_KEY = os.getenv("API_GATEWAY_KEY")
print("API gateway key:", API_GATEWAY_KEY)  # debug

# FastAPI app
app = FastAPI(title="Secure LLM Gateway")

# Standard Python logger
logger = logging.getLogger(__name__)


@app.post("/generate")
async def generate(request: Request, role: str = Depends(verify_api_key)):
    """
    Endpoint to generate LLM output.
    Performs:
    - Input validation
    - RBAC authorization
    - Rate limiting (token bucket)
    - LLM call
    - Structured logging
    """
    start_time = time.time()

    try:
        # Parse JSON body
        data = await request.json()
        prompt = data.get("prompt", "")

        # Input validation
        validate_prompt(prompt)

        # Authorization
        authorize(role, "generate")

        # Rate limiting
        check_token_bucket_limit(role)

        # Call LLM (mock or real)
        response = query_llm(prompt)

        latency_ms = round((time.time() - start_time) * 1000, 2)

        # Structured log
        log_event({
            "event": "generate_success",
            "role": role,
            "prompt_length": len(prompt),
            "latency_ms": latency_ms
        })

        logger.info(
            f"LLM request success: role={role}, prompt_len={len(prompt)}")
        return {"response": response}

    except ValidationError as ve:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        log_event({
            "event": "generate_validation_error",
            "role": role,
            "error": str(ve),
            "latency_ms": latency_ms
        })
        logger.warning(f"Validation failed: {ve}")
        return {"error": str(ve)}

    except LLMGatewayError as le:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        log_event({
            "event": "generate_llm_error",
            "role": role,
            "error": str(le),
            "latency_ms": latency_ms
        })
        logger.error(f"LLM request failed: {le}")
        return {"error": str(le)}

    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        log_event({
            "event": "generate_unhandled_error",
            "role": role,
            "error": str(e),
            "latency_ms": latency_ms
        })
        logger.exception("Unhandled error in /generate")
        return {"error": "Internal server error"}
