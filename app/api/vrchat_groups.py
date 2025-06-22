from fastapi import APIRouter, HTTPException
import httpx
import json
from app.env import CLIENT_NAME, API_BASE, TOKEN_FILE

router = APIRouter()

def load_token():
    if not TOKEN_FILE.exists():
        return None
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)

@router.get("/groups/{group_id}")
async def get_groups(group_id: str):
    token = load_token()
    if not token:
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = token.get("auth_cookie")
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    params = {
        "includeRoles": "true",
        "purpose": "group"
    }
    url = f"{API_BASE}/groups/{group_id}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch group info: {r.text}")

    return r.json()

@router.get("/groups/{group_id}/instances")
async def get_groups_instances(group_id: str, user_id: str):
    token = load_token()
    if not token:
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = token.get("auth_cookie")
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    url = f"{API_BASE}/groups/{group_id}/instances"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch groups instances info: {r.text}")

    return r.json()

@router.get("/groups/{group_id}/posts")
async def get_groups_posts(group_id: str):
    token = load_token()
    if not token:
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = token.get("auth_cookie")
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    params = {
        "n": "10",
        "offset": "0",  
        "publicOnly": False
    }
    url = f"{API_BASE}/groups/{group_id}/posts"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch groups posts info: {r.text}")

    return r.json()


@router.get("/groups/{group_id}/bans")
async def get_groups_bans(group_id: str):
    token = load_token()
    if not token:
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = token.get("auth_cookie")
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    params = {
        "n": "51",
        "offset": "0"
    }
    url = f"{API_BASE}/groups/{group_id}/bans"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch groups bans info: {r.text}")

    return r.json()

@router.get("/groups/{group_id}/roles")
async def get_groups_roles(group_id: str):
    token = load_token()
    if not token:
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = token.get("auth_cookie")
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    url = f"{API_BASE}/groups/{group_id}/roles"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch groups roles info: {r.text}")

    return r.json()

@router.get("/groups/{group_id}/members")
async def get_groups_members(group_id: str):
    token = load_token()
    if not token:
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = token.get("auth_cookie")
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    params = {
        "n": "25",
        "offset": "0"
    }
    url = f"{API_BASE}/groups/{group_id}/members"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch groups members info: {r.text}")

    return r.json()