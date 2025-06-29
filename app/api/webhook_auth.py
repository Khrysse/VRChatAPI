from fastapi import APIRouter
import threading

router = APIRouter()

shared_state = {
    "status": "IDLE",  # IDLE, NEED_CREDENTIALS, NEED_2FA, CONNECTED, ERROR
    "last_error": None,
    "credentials": None,  # {"username": ..., "password": ...}
    "2fa_code": None,
    "display_name": None,
    "user_id": None
}
state_lock = threading.Lock()

@router.get("/status")
def get_status():
    with state_lock:
        return {
            "status": shared_state["status"],
            "last_error": shared_state["last_error"],
            "display_name": shared_state["display_name"],
            "user_id": shared_state["user_id"]
        }

@router.get("/status/short")
def get_status_short():
    with state_lock:
        return {
            "status": shared_state["status"],
            "last_error": shared_state["last_error"]
        }

@router.get("/vrchat/connected")
def get_connected():
    with state_lock:
        if shared_state["status"] == "CONNECTED":
            return {
                "display_name": shared_state["display_name"],
                "user_id": shared_state["user_id"]
            }
        return {}

@router.post("/login")
def post_login(data: dict):
    with state_lock:
        shared_state["credentials"] = {
            "username": data.get("username"),
            "password": data.get("password")
        }
        shared_state["status"] = "GOT_CREDENTIALS"
        shared_state["last_error"] = None
    return {"message": "Credentials received"}

@router.get("/login")
def get_login():
    with state_lock:
        creds = shared_state["credentials"]
        if creds:
            shared_state["credentials"] = None
            return creds
        return {}

@router.post("/2fa")
def post_2fa(data: dict):
    with state_lock:
        shared_state["2fa_code"] = data.get("code")
        shared_state["status"] = "GOT_2FA"
        shared_state["last_error"] = None
    return {"message": "2FA code received"}

@router.get("/2fa")
def get_2fa():
    with state_lock:
        code = shared_state["2fa_code"]
        if code:
            shared_state["2fa_code"] = None
            return {"code": code}
        return {}

@router.post("/status")
def set_status(data: dict):
    with state_lock:
        shared_state["status"] = data.get("status", shared_state["status"])
        if "last_error" in data:
            shared_state["last_error"] = data["last_error"]
        if "display_name" in data:
            shared_state["display_name"] = data["display_name"]
        if "user_id" in data:
            shared_state["user_id"] = data["user_id"]
    return {"message": "Status updated"}
