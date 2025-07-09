from dotenv import load_dotenv
import os
import httpx
from fastapi import APIRouter, HTTPException
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

CLIENT_NAME = os.getenv("CLIENT_NAME", "default-client-name")
API_BASE = os.getenv("VRCHAT_API_BASE", "https://api.vrchat.cloud/api/1")
TOKEN_FILE = Path(os.getenv("TOKEN_FILE", "data/auth/account.json"))
IS_DISTANT = os.getenv("IS_DISTANT", "false").lower() in ("1", "true", "yes")
DISTANT_URL_CONTEXT = os.getenv("DISTANT_URL_CONTEXT", "")
PORT = os.environ.get("PORT", "8080")
API_IS_PUBLIC = os.environ.get("API_IS_PUBLIC", "true").lower() in ("1", "true", "yes")
API_DOMAIN = os.environ.get("API_DOMAIN", "unstealable.cloud")
CORS_ALLOWED_ORIGINS = [
    f"https://{API_DOMAIN}",
    f"https://*.{API_DOMAIN}"
]
