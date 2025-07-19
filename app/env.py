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

# CORS configuration
CORS_ALLOWED_ORIGINS_ENV = os.environ.get("CORS_ALLOWED_ORIGINS", "unstealable.cloud")

# If not public, build CORS origins list based on the domain
if not API_IS_PUBLIC and CORS_ALLOWED_ORIGINS_ENV:
    API_DOMAIN = CORS_ALLOWED_ORIGINS_ENV
    CORS_ALLOWED_ORIGINS = []
    
    # Add main domain
    CORS_ALLOWED_ORIGINS.append(f"https://{API_DOMAIN}")
    CORS_ALLOWED_ORIGINS.append(f"http://{API_DOMAIN}")
    
    # Add common subdomains
    common_subdomains = [
        "www",
        "api", 
        "hook",
        "vrchat-bridge",
        "vrclookup",
        "app",
        "dashboard"
    ]
    
    for subdomain in common_subdomains:
        CORS_ALLOWED_ORIGINS.append(f"https://{subdomain}.{API_DOMAIN}")
        CORS_ALLOWED_ORIGINS.append(f"http://{subdomain}.{API_DOMAIN}")
else:
    # Public mode or no domain specified
    CORS_ALLOWED_ORIGINS = []
    API_DOMAIN = CORS_ALLOWED_ORIGINS_ENV

# Function to check if any subdomain is allowed
def is_subdomain_allowed(origin: str) -> bool:
    """Check if origin is any subdomain of our domain (more restrictive)"""
    import re
    if not origin or len(origin) > 253:  # Max domain length
        return False
    
    # Pattern: https://subdomain.domain.com (max 2 levels, alphanumeric + hyphens)
    pattern = re.compile(r'^https?://[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.' + re.escape(API_DOMAIN) + r'$')
    match = pattern.match(origin)
    
    if match:
        # Additional validation: subdomain should not be too long or contain suspicious patterns
        subdomain = origin.split("://")[1].split(".")[0]
        if len(subdomain) > 63 or "--" in subdomain:  # RFC limits
            return False
        return True
    
    return False
