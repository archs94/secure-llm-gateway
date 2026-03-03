import os
import json
from fastapi import Request, HTTPException

# Do NOT read API_GATEWAY_KEY at import time
# API key and RBAC roles will be read inside functions


def verify_api_key(request: Request):
    """
    Verify API key from header x-api-key.
    Returns the user role if valid.
    """
    api_gateway_key = os.getenv("API_GATEWAY_KEY")
    rbac_roles = json.loads(os.getenv("RBAC_ROLES", "{}"))

    key = request.headers.get("x-api-key")
    print("Received API key:", key)
    print("API gateway key:", api_gateway_key)

    if key != api_gateway_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Use header x-role to specify role
    role = request.headers.get("x-role", "guest")
    return role


def authorize(role: str, action: str):
    """
    Check if the role is allowed to perform the action.
    Raises 403 if forbidden.
    """
    rbac_roles = json.loads(os.getenv("RBAC_ROLES", "{}"))
    allowed_actions = rbac_roles.get(role, [])
    if "*" in allowed_actions or action in allowed_actions:
        return True
    raise HTTPException(status_code=403, detail="Forbidden")
