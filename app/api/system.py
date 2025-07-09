from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.vrchat_context import get_context_safely
router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.get("/vrchat/connected")
async def vrchat_connected():
    vrchat = get_context_safely()
    if vrchat and getattr(vrchat, "auth_cookie", None) and vrchat.auth_cookie.startswith("authcookie_"):
        return {"connected": True, "display_name": getattr(vrchat, "display_name", None), "user_id": getattr(vrchat, "user_id", None)}
    return {"connected": False, "display_name": None, "user_id": None}

@router.get("/status")
async def status():
    vrchat = get_context_safely()
    if vrchat and getattr(vrchat, "auth_cookie", None) and vrchat.auth_cookie.startswith("authcookie_"):
        return {"accountStatus": "ok", "auth": True}
    return {"accountStatus": "not_authenticated", "auth": False}