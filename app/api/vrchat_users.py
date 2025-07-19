from fastapi import APIRouter, HTTPException, Query
import httpx
import json
from typing import Optional
from app.env import CLIENT_NAME, API_BASE
from app.vrchat_context import get_context_safely
from app.utils import (
    validate_vrchat_user_id,
    validate_pagination_params,
    make_vrchat_request,
    handle_vrchat_response
)
router = APIRouter()

@router.get("/users/me")
async def get_bot_users_profile():
    """Get the current bot's user profile."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Authentication required")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": vrchat.auth_cookie}
    url = f"{API_BASE}/users/{vrchat.user_id}"

    response = await make_vrchat_request(url, headers, cookies)
    return handle_vrchat_response(response, "get bot profile")

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get a user's profile by user ID."""
    # Validate input
    user_id = validate_vrchat_user_id(user_id)
    
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Authentication required")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": vrchat.auth_cookie}
    url = f"{API_BASE}/users/{user_id}"

    response = await make_vrchat_request(url, headers, cookies)
    return handle_vrchat_response(response, "get user")

@router.get("/users/{user_id}/friends/status")
async def get_user_friend_status(user_id: str):
    """Get the friend status of a user by user ID."""
    # Validate input
    user_id = validate_vrchat_user_id(user_id)
    
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Authentication required")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": vrchat.auth_cookie}
    url = f"{API_BASE}/users/{user_id}/friendStatus"

    response = await make_vrchat_request(url, headers, cookies)
    return handle_vrchat_response(response, "get friend status")

@router.get("/users/{user_id}/groups")
async def get_user_groups(user_id: str):
    """Get the groups a user belongs to by user ID."""
    # Validate input
    user_id = validate_vrchat_user_id(user_id)
    
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Authentication required")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": vrchat.auth_cookie}
    url = f"{API_BASE}/users/{user_id}/groups"

    response = await make_vrchat_request(url, headers, cookies)
    return handle_vrchat_response(response, "get user groups")

@router.get("/users/{user_id}/worlds")
async def get_user_worlds(user_id: str, n: int = Query(default=100), offset: int = Query(default=0)):
    """Get the worlds created by a user by user ID."""
    # Validate inputs
    user_id = validate_vrchat_user_id(user_id)
    offset, n = validate_pagination_params(offset, n)
    
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Authentication required")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": vrchat.auth_cookie}
    params = {
        "releaseStatus": "public",
        "sort": "updated",
        "order": "descending",
        "userId": user_id,
        "n": str(n),
        "offset": str(offset)
    }
    
    # Use httpx client with params
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{API_BASE}/worlds", headers=headers, cookies=cookies, params=params)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="VRChat API timeout")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="VRChat API unavailable")
        
    return handle_vrchat_response(response, "get user worlds")