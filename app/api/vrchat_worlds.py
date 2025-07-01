from fastapi import APIRouter, HTTPException
import httpx
import json
from app.env import CLIENT_NAME, API_BASE
from app.vrchat_context import get_context_safely
router = APIRouter()

@router.get("/worlds/{world_id}")
async def get_worlds(world_id: str):
    """Get information about a specific worlds by its ID."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    url = f"{API_BASE}/worlds/{world_id}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch world info: {r.text}")

    return r.json()

@router.get("/worlds/{world_id}/metadata")
async def get_worlds_metadata(world_id: str):
    """Get metadata about a specific worlds by its ID."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    url = f"{API_BASE}/worlds/{world_id}/metadata"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch world info: {r.text}")

    return r.json()

@router.get("/worlds/{world_id}/{instance_id}")
async def get_specific_instance_by_world(world_id: str, instance_id: str):
    """Get information about a specific world instance by its ID."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    url = f"{API_BASE}/worlds/{world_id}/{instance_id}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch world instance info: {r.text}")

    return r.json()