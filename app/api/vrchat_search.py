from fastapi import APIRouter, HTTPException
import httpx
import json
from app.env import CLIENT_NAME, API_BASE, TOKEN_FILE
from app.vrchat_context import VRChatContext

router = APIRouter()

def load_context():
    VRChatContext.load()

def load_token():
    if not TOKEN_FILE.exists():
        return None
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)

@router.get("/auth/exists/{type}/{text}")
async def get_if_exists_per_type(type: str, text: str):
    load_context()
    vrchat = VRChatContext.get()

    if type not in ["username", "email"]:
        raise HTTPException(status_code=400, detail="Invalid type, must be 'username' or 'email'")
    
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if not text.startswith("usr_") or text.startswith("group_"):
        raise HTTPException(status_code=400, detail="Invalid text format, must start with 'usr_' or 'group_'")

    if not vrchat:
        raise HTTPException(status_code=401, detail="Token not found, please authenticate first")

    auth_cookie = vrchat.auth_cookie
    if not auth_cookie:
        raise HTTPException(status_code=401, detail="Auth cookie missing in token")

    headers = {"User-Agent": CLIENT_NAME}
    cookies = {"auth": auth_cookie}
    url = f"{API_BASE}/auth/exists?{type}={text}{'&displayName=' + text if type == 'username' else ''}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers, cookies=cookies)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch if {type} exists: {r.text}")

    return r.json()