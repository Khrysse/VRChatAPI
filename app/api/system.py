from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.vrchat_context import get_context_safely
router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.get("/status")
def status_check():
    vrchat = get_context_safely()
    if not vrchat.auth_cookie or not vrchat.auth_cookie.startswith("authcookie_"):
        return {"accountStatus": "not authenticated"}
    return {"accountStatus": "ok"}

@router.get("/vrchat/connected")
def get_if_vrchat_account_is_connected():
    vrchat = get_context_safely()
    return {
        "display_name": getattr(vrchat, "display_name", None),
        "user_id": getattr(vrchat, "user_id", None)
    }