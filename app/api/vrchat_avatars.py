from fastapi import APIRouter, HTTPException
import httpx
import json
from app.env import CLIENT_NAME, API_BASE
from app.vrchat_context import get_context_safely
router = APIRouter()

@router.get("/avatars/{avatar_id}")
async def get_worlds(avatar_id: str):
    """Get information about a specific avatars by its ID."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    url = f"{API_BASE}/avatars/{avatar_id}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch avatars info: {r.text}")

    return r.json()