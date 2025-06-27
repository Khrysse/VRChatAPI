from fastapi import APIRouter
from app.vrchat_context import VRChatContext

def load_context():
    VRChatContext.load()
vrchat = VRChatContext.get()

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.get("/status")
def status_check():
    return {"status": "ok" if vrchat.auth_cookie else "not authenticated"}
