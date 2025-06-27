import httpx
import base64
import json
from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent)) 
from app.env import CLIENT_NAME, API_BASE, TOKEN_FILE, IS_DISTANT
from app.vrchat_context import VRChatContext

def verify_auth_cookie(auth_cookie):
    cookies = {"auth": auth_cookie}
    headers = {"User-Agent": CLIENT_NAME}
    with httpx.Client(base_url=API_BASE, cookies=cookies, headers=headers) as client:
        r = client.get("/auth")
        return r.status_code == 200 and r.json().get("ok", False)

def get_or_create_token():
    if IS_DISTANT:
        print("⚠️ Running in distant environment, using VRChatContext.")
        try:
            VRChatContext.load()
            token = VRChatContext.get()
            if not verify_auth_cookie(token.auth_cookie):
                print("❌ Remote token invalid. Please regenerate the token and update the distant source.")
                return None
            print("🔓 Auth ready from distant environment.")
            return {
                "manual_username": token.manual_username,
                "displayName": token.display_name,
                "user_id": token.user_id,
                "auth": token.auth_header,
                "auth_cookie": token.auth_cookie
            }
        except Exception as e:
            print("❌ Failed to initialize VRChatContext:", e)
            return None

    if not TOKEN_FILE.exists():
        return None

    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)

    created = datetime.fromisoformat(data.get("created_at", "2000-01-01T00:00:00+00:00"))
    if datetime.now(timezone.utc) - created > timedelta(days=30):
        print("⚠️ Token expired. Reconnection required.")
        return None

    if not verify_auth_cookie(data.get("auth_cookie", "")):
        print("❌ Local token invalid. Please log in again.")
        return None

    print("🟢 Local token valid.")
    return data

def save_token(data):
    data["created_at"] = datetime.now(timezone.utc).isoformat()
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=4)

def login():
    print("🔐 Connecting to VRChat")
    manual_username = input("Username: ")
    password = input("Password: ")

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
            return None

        data = r.json()

        if "requiresTwoFactorAuth" in data:
            mfa_types = data["requiresTwoFactorAuth"]
            print(f"🔐 2FA required: {mfa_types}")

            client.headers.pop("Authorization", None)

            if "otp" in mfa_types:
                code = input("Code 2FA (TOTP): ")
                verify_endpoint = "/auth/twofactorauth/verify"
            elif "emailOtp" in mfa_types:
                code = input("Code 2FA (email): ")
                verify_endpoint = "/auth/twofactorauth/emailotp/verify"
            else:
                print("❌ Unknown 2FA type:", mfa_types)
                return None

            r2 = client.post(verify_endpoint, json={"code": code})

            if r2.status_code != 200 or not r2.json().get("verified", False):
                print("❌ 2FA verification failed:", r2.text)
                return None
            print("✅ 2FA verified!")

            r3 = client.get("/auth/user")
            if r3.status_code != 200:
                print("❌ Failed to fetch user data after 2FA:", r3.text)
                return None

            data = r3.json()

        auth_cookie = None
        for cookie in client.cookies.jar:
            if cookie.name == "auth":
                auth_cookie = cookie.value
                break

        if not auth_cookie:
            print("❌ Auth cookie not found after login.")
            return None

        if not verify_auth_cookie(auth_cookie):
            print("❌ Auth cookie invalid.")
            return None

        print("✅ Connected and verified.")

        display_name = data.get("displayName", manual_username)
        user_id = data.get("id", "")

        return {
            "manual_username": manual_username,
            "displayName": display_name,
            "user_id": user_id,
            "auth": b64,
            "auth_cookie": auth_cookie
        }

if __name__ == "__main__":
    token_data = get_or_create_token()
    if token_data:
        print("🔓 Auth ready. Token stored.")
        if not IS_DISTANT:
            save_token(token_data)
    else:
        print("❌ Unable to obtain a valid token.")
