from fastapi import APIRouter, HTTPException
import httpx
import json
from app.env import CLIENT_NAME, API_BASE
from app.vrchat_context import get_context_safely
router = APIRouter()

@router.get("/auth/exists/{type}/{text}")
async def get_if_exists_per_type(type: str, text: str):
    """Check if a user or world exists by username or email."""
    if type not in ["username", "email"]:
        raise HTTPException(status_code=400, detail="Invalid type, must be 'username' or 'email'")
    
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    headers = {"User-Agent": CLIENT_NAME}
    url = f"{API_BASE}/auth/exists?{type}={text}{'&displayName=' + text if type == 'username' else ''}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch if {type} exists: {r.text}")

    return r.json()

@router.get("/search/{type}/{search_text}?n={n}")
async def search_by_type(type: str, search_text: str, n: int = 12):
    """Search for users or worlds by type and search text."""
    if type not in ["users", "worlds"]:
        raise HTTPException(status_code=400, detail="Invalid type, must be 'users' or 'worlds'")
    
    if not search_text:
        raise HTTPException(status_code=400, detail="Search text cannot be empty")
    
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    params = {
        "sort": "relevance",
        "fuzzy": "false",
        "search": search_text,
        "n": str(n)
    }   
    url = f"{API_BASE}/{type}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to search {type} by: {r.text}")

    return r.json()