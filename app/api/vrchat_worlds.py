from fastapi import APIRouter, HTTPException
import httpx
import json
from app.env import CLIENT_NAME, API_BASE
from app.vrchat_context import get_context_safely
from app.utils import (
    validate_vrchat_world_id,
    validate_vrchat_instance_id,
    make_vrchat_request,
    handle_vrchat_response
)
router = APIRouter()

@router.get("/worlds/{world_id}")
async def get_worlds(world_id: str):
    """Get information about a specific world by its ID."""
    # Validate input
    world_id = validate_vrchat_world_id(world_id)
    
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Authentication required")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": vrchat.auth_cookie}
    url = f"{API_BASE}/worlds/{world_id}"

    response = await make_vrchat_request(url, headers, cookies)
    return handle_vrchat_response(response, "get world")

@router.get("/worlds/{world_id}/metadata")
async def get_worlds_metadata(world_id: str):
    """Get metadata about a specific world by its ID."""
    # Validate input
    world_id = validate_vrchat_world_id(world_id)
    
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Authentication required")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": vrchat.auth_cookie}
    url = f"{API_BASE}/worlds/{world_id}/metadata"

    response = await make_vrchat_request(url, headers, cookies)
    return handle_vrchat_response(response, "get world metadata")

@router.get("/worlds/{world_id}/{instance_id}")
async def get_specific_instance_by_world(world_id: str, instance_id: str):
    """Get information about a specific world instance by its ID."""
    # Validate inputs
    world_id = validate_vrchat_world_id(world_id)
    instance_id = validate_vrchat_instance_id(instance_id)
    
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Authentication required")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": vrchat.auth_cookie}
    url = f"{API_BASE}/worlds/{world_id}/{instance_id}"

    response = await make_vrchat_request(url, headers, cookies)
    return handle_vrchat_response(response, "get world instance")