from fastapi import APIRouter, HTTPException
import httpx
import json
from app.env import CLIENT_NAME, API_BASE
from app.vrchat_context import get_context_safely
router = APIRouter()

@router.get("/groups/{group_id}")
async def get_groups(group_id: str):
    """Get information about a specific group by its ID."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
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
async def get_groups_instances(group_id: str):
    """Get instances of a specific group by its ID."""
    """This endpoint requires the group ID to be passed as a query parameter."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
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

@router.get("/groups/{group_id}/posts?n={n}&offset={offset}")
async def get_groups_posts(group_id: str, n: int = 10, offset: int = 0):
    """Get posts of a specific group by its ID."""
    """This endpoint requires the group ID to be passed as a query parameter."""
    """The group ID is used to fetch the posts related to the group."""
    """The posts are returned in a paginated format with a default of 10 posts per page."""
    """You can adjust the number of posts per page by changing the 'n' parameter."""
    """The 'offset' parameter can be used to fetch posts starting from a specific index."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    params = {
        "n": str(n),
        "offset": str(offset),  
        "publicOnly": False
    }
    url = f"{API_BASE}/groups/{group_id}/posts"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch groups posts info: {r.text}")

    return r.json()


@router.get("/groups/{group_id}/bans?n={n}&offset={offset}")
async def get_groups_bans(group_id: str, n: int = 51, offset: int = 0):
    """Get bans of a specific group by its ID."""
    """This endpoint requires the group ID to be passed as a query parameter."""
    """The group ID is used to fetch the bans related to the group."""
    """The bans are returned in a paginated format with a default of 51 bans per page."""
    """You can adjust the number of bans per page by changing the 'n' parameter."""
    """The 'offset' parameter can be used to fetch bans starting from a specific index."""
    """This endpoint is useful for managing group bans and retrieving information about banned users."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    params = {
        "n": str(n),
        "offset": str(offset),
    }
    url = f"{API_BASE}/groups/{group_id}/bans"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch groups bans info: {r.text}")

    return r.json()

@router.get("/groups/{group_id}/roles")
async def get_groups_roles(group_id: str):
    """Get roles of a specific group by its ID."""
    """This endpoint requires the group ID to be passed as a query parameter."""
    """The group ID is used to fetch the roles related to the group."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
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

@router.get("/groups/{group_id}/members?n={n}&offset={offset}")
async def get_groups_members(group_id: str, n: int = 25, offset: int = 0):
    """Get members of a specific group by its ID."""
    """This endpoint requires the group ID to be passed as a query parameter."""
    """The group ID is used to fetch the members related to the group."""
    """The members are returned in a paginated format with a default of 25 members per page."""
    """You can adjust the number of members per page by changing the 'n' parameter."""
    """The 'offset' parameter can be used to fetch members starting from a specific index."""
    """This endpoint is useful for managing group memberships and retrieving information about group members."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    params = {
        "n": str(n),
        "offset": str(offset),
    }
    url = f"{API_BASE}/groups/{group_id}/members"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch groups members info: {r.text}")

    return r.json()

@router.get("/groups/me")
async def get_bot_groups_profile():
    """Get the current bot's groups profile."""
    """This endpoint retrieves the groups profile of the bot currently authenticated."""
    """It requires the bot to be authenticated with a valid auth cookie."""
    """The response includes information about the bot's groups, such as group IDs, names, and roles."""
    """This endpoint is useful for managing the bot's group memberships and retrieving information about the groups it belongs to."""
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    url = f"{API_BASE}/groups/me"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch bot groups profile info: {r.text}")

    return r.json()