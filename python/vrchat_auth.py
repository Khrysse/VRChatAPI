import httpx
import base64
import json
from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).resolve().parent.parent)) 
from app.env import CLIENT_NAME, API_BASE, TOKEN_FILE, IS_DISTANT, DISTANT_URL_CONTEXT 
from app.vrchat_context import get_context_safely

WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "http://localhost:8080/webhook/auth")

def verify_auth_cookie(auth_cookie):
    cookies = {"auth": auth_cookie}
    headers = {"User-Agent": CLIENT_NAME}
    with httpx.Client(base_url=API_BASE, cookies=cookies, headers=headers) as client:
        r = client.get("/auth")
        return r.status_code == 200 and r.json().get("ok", False)

def save_token(data):
    data["created_at"] = datetime.now(timezone.utc).isoformat()
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_token():
    if not TOKEN_FILE.exists():
        return None
    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
    created = datetime.fromisoformat(data.get("created_at", "2000-01-01T00:00:00+00:00"))
    if datetime.now(timezone.utc) - created > timedelta(days=30):
        print("⚠️ Token expired. Reconnection required.")
        return None
    return data

def login_via_webhook():
    import time
    # Demande credentials via webhook
    httpx.post(f"{WEBHOOK_URL}/status", json={"status": "NEED_CREDENTIALS", "last_error": None, "display_name": None, "user_id": None})
    print("🔗 Waiting for credentials via web interface (hook)...")
    for _ in range(300):
        r = httpx.get(f"{WEBHOOK_URL}/status")
        if r.status_code == 200 and r.json().get("status") == "GOT_CREDENTIALS":
            creds = httpx.get(f"{WEBHOOK_URL}/login").json()
            username = creds.get("username")
            password = creds.get("password")
            if username and password:
                break
        time.sleep(1)
    else:
        print("⏰ Timeout credentials.")
        httpx.post(f"{WEBHOOK_URL}/status", json={"status": "IDLE", "last_error": "Timeout credentials"})
        return None
    manual_username = username
    password = password
    creds = f"{manual_username}:{password}"
    b64 = base64.b64encode(creds.encode()).decode()
    auth_header = f"Basic {b64}"
    headers = {
        "Authorization": auth_header,
        "User-Agent": CLIENT_NAME
    }
    with httpx.Client(base_url=API_BASE, headers=headers) as client:
        r = client.get("/auth/user")
        if r.status_code != 200:
            print("❌ Connection failed:", r.text)
            httpx.post(f"{WEBHOOK_URL}/status", json={"status": "IDLE", "last_error": "Login failed"})
            return None
        data = r.json()
        if "requiresTwoFactorAuth" in data:
            mfa_types = data["requiresTwoFactorAuth"]
            print(f"🔐 2FA required: {mfa_types}")
            httpx.post(f"{WEBHOOK_URL}/status", json={"status": "NEED_2FA"})
            client.headers.pop("Authorization", None)
            for _ in range(180):
                r2fa = httpx.get(f"{WEBHOOK_URL}/2fa")
                code = r2fa.json().get("code")
                if code:
                    break
                time.sleep(1)
            else:
                print("⏰ Timeout 2FA.")
                httpx.post(f"{WEBHOOK_URL}/status", json={"status": "IDLE", "last_error": "Timeout 2FA"})
                return None
            verify_endpoint = "/auth/twofactorauth/verify" if "otp" in mfa_types else "/auth/twofactorauth/emailotp/verify"
            r2 = client.post(verify_endpoint, json={"code": code})
            if r2.status_code != 200 or not r2.json().get("verified", False):
                print("❌ 2FA verification failed:", r2.text)
                httpx.post(f"{WEBHOOK_URL}/status", json={"status": "IDLE", "last_error": "2FA failed"})
                return None
            print("✅ 2FA verified!")
            r3 = client.get("/auth/user")
            if r3.status_code != 200:
                print("❌ Failed to fetch user data after 2FA:", r3.text)
                httpx.post(f"{WEBHOOK_URL}/status", json={"status": "IDLE", "last_error": "Failed to fetch user after 2FA"})
                return None
            data = r3.json()
    auth_cookie = None
    for cookie in client.cookies.jar:
        if cookie.name == "auth":
            auth_cookie = cookie.value
            break
    if not auth_cookie:
        print("❌ Auth cookie not found after login.")
        httpx.post(f"{WEBHOOK_URL}/status", json={"status": "IDLE", "last_error": "No auth cookie"})
        return None
    if not verify_auth_cookie(auth_cookie):
        print("❌ Auth cookie invalid.")
        httpx.post(f"{WEBHOOK_URL}/status", json={"status": "IDLE", "last_error": "Invalid auth cookie"})
        return None
    display_name = data.get("displayName", manual_username)
    user_id = data.get("id", "")
    print("✅ Connected and verified.")
    httpx.post(f"{WEBHOOK_URL}/status", json={"status": "CONNECTED", "display_name": display_name, "user_id": user_id})
    return {
        "manual_username": manual_username,
        "displayName": display_name,
        "user_id": user_id,
        "auth": b64,
        "auth_cookie": auth_cookie
    }

def get_or_create_token():
    token = load_token()
    if token:
        print("🔑 Found saved token, verifying...")
        if verify_auth_cookie(token.get("auth_cookie", "")):
            print("🟢 Token already valid.")
            return token
        else:
            print("⚠️ Saved token invalid, need to login again.")
    return login_via_webhook()

if __name__ == "__main__":
    token_data = get_or_create_token()
    if token_data:
        print("🔓 Auth ready. Token stored.")
        if not IS_DISTANT:
            save_token(token_data)
    else:
        print("❌ Unable to obtain a valid token.")
