from fastapi import FastAPI
from app.api.vrchat_users import router as users
from app.api.vrchat_groups import router as groups
from app.api.system import router as system

app = FastAPI(
    title="K-API",
    description="""
    K-API is a fast, secure, and lightweight proxy API for VRChat.  
    It handles authentication via VRChat’s official API, including 2FA support,  
    and provides cached endpoints for user and group information retrieval.  

    This project is designed for developers who want a hassle-free way  
    to integrate VRChat data into their apps without managing sessions or tokens manually.  

    Features:
    - Automatic token management with 2FA handling
    - Public and private VRChat data endpoints
    - Response caching for performance
    - Easy deployment on self-hosted servers (YunoHost compatible)
    
    Built with FastAPI and async HTTPX for high performance and reliability.
    """,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
    contact={"name": "Kryscau", "url": "https://vrchat.com/home/user/usr_323befe7-edbc-46fe-af9d-560f7e6b290c", "email": "kryscau@kvs.fyi" }
)
prefix = "/api"

app.include_router(users, prefix=prefix, tags=["Users"])
app.include_router(groups, prefix=prefix, tags=["Groups"])
app.include_router(system, prefix=prefix, tags=["System"])