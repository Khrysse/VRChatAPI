from http.client import HTTPException
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os
import httpx
from fastapi import HTTPException
import sys
from app.env import IS_DISTANT, DISTANT_URL_CONTEXT, TOKEN_FILE

@dataclass
class VRChatData:
    display_name: str
    user_id: str
    auth_cookie: str
    auth_header: str
    manual_username: str

class VRChatContext:
    _instance: Optional["VRChatContext"] = None

    def __init__(self):
        self._token: Optional[VRChatData] = None

    @classmethod
    def load(cls):
        if IS_DISTANT:
            cls._load_from_remote()
        else:
            cls._load_from_local()

    @classmethod
    def _load_from_local(cls, path: Path = Path(TOKEN_FILE)):
        if not path.exists():
            raise FileNotFoundError(f"{TOKEN_FILE} file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cls._set_instance(data)

    @classmethod
    def _load_from_remote(cls):
        remote_url = DISTANT_URL_CONTEXT
        if not remote_url:
            raise EnvironmentError("DISTANT_URL_CONTEXT is not defined in environment")

        try:
            response = httpx.get(remote_url, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            cls._set_instance(data)
        except httpx.RequestError as e:
            raise ConnectionError(f"Could not fetch remote VRChat Data: {e}")

    @classmethod
    def _set_instance(cls, data: dict):
        cls._instance = cls()
        cls._instance._token = VRChatData(
            display_name=data.get("displayName", ""),
            user_id=data.get("user_id", ""),
            auth_cookie=data.get("auth_cookie", ""),
            auth_header=data.get("auth", ""),
            manual_username=data.get("manual_username", "")
        )

    @classmethod
    def get(cls) -> VRChatData:
        if not cls._instance or not cls._instance._token:
            raise RuntimeError("VRChatContext not initialized. Call VRChatContext.load() first.")
        return cls._instance._token

def get_context_safely():
    try:
        VRChatContext.load()
        return VRChatContext.get()
    except Exception as e:
        if "uvicorn" in sys.argv[0] or "main.py" in sys.argv[0]:
            raise HTTPException(status_code=500, detail=f"VRChatContext init failed: {str(e)}")
        else:
            raise RuntimeError(f"VRChatContext init failed: {str(e)}")