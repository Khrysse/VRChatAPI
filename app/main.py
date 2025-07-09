import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.vrchat_search import router as search
from app.api.vrchat_users import router as users
from app.api.vrchat_groups import router as groups
from app.api.system import router as system
from app.vrchat_context import get_context_safely
from app.api.webhook_auth import router as webhook_auth
from app.env import PORT

def create_main_app():
    app = FastAPI(
        title="US VRChat Bridge",
        description="""
VRChat Bridge by Unstealable is a fast, secure, and lightweight proxy API for VRChat.

It handles authentication via VRChat’s official API, including 2FA support, and provides cached endpoints for user and group information retrieval.

This project is designed for developers who want a hassle-free way to integrate VRChat data into their apps without managing sessions or tokens manually.

Features:
- Automatic token management with 2FA handling
- Public and private VRChat data endpoints
- Response caching for performance
- Easy deployment on self-hosted servers

Built with FastAPI and async HTTPX for high performance and reliability.
""",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/api.json",
        contact={"name": "UnStealable", "url": "https://vrchat.com/home/user/usr_3e354294-5925-42bb-a5e6-511c39a390eb"}
    )

    prefix = "/api"
    try:
        vrchat = get_context_safely()
        if vrchat and getattr(vrchat, "auth_cookie", None) and vrchat.auth_cookie.startswith("authcookie_"):
            app.include_router(users, prefix=prefix, tags=["Users"])
            app.include_router(groups, prefix=prefix, tags=["Groups"])
            app.include_router(search, prefix=prefix, tags=["Search"])
        else:
            print("[WARN] No valid VRChat token found. Only public/system endpoints will be available.", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to load VRChat context: {e}", flush=True)
        print("[WARN] Only public/system endpoints will be available.", flush=True)
    app.include_router(system, prefix=prefix, tags=["System"])

    return app


def create_auth_webhook_app():
    from fastapi import FastAPI
    app = FastAPI(title="K-API Auth Webhook")
    app.include_router(webhook_auth, prefix="/webhook/auth", tags=["Auth Webhook"])
    app.include_router(system, prefix="/api", tags=["System"])
    return app

if __name__ == "__main__":
    if "--auth-mode" in sys.argv:
        uvicorn.run(create_auth_webhook_app(), host="0.0.0.0", port=PORT, reload=False)
    else:
        uvicorn.run(create_main_app(), host="0.0.0.0", port=PORT, reload=True)

app = create_main_app() 
app.add_middleware(
    CORSMiddleware,
        allow_origins=["*"],
            allow_credentials=True,
                allow_methods=["GET", "POST", "OPTIONS"], 
                    allow_headers=["*"], 
                    )