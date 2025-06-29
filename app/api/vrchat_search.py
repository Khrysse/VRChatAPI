from fastapi import APIRouter, HTTPException
import httpx
import json
from app.env import CLIENT_NAME, API_BASE
router = APIRouter()

@router.get("/auth/exists/{type}/{text}")
async def get_if_exists_per_type(type: str, text: str):
    if type not in ["username", "email"]:
        raise HTTPException(status_code=400, detail="Invalid type, must be 'username' or 'email'")
    
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if not (text.startswith("usr_") or text.startswith("group_")):
        raise HTTPException(status_code=400, detail="Invalid text format, must start with 'usr_' or 'group_'")

    headers = {"User-Agent": CLIENT_NAME}
    url = f"{API_BASE}/auth/exists?{type}={text}{'&displayName=' + text if type == 'username' else ''}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch if {type} exists: {r.text}")

    return r.json()