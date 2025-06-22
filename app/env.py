from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

CLIENT_NAME = os.getenv("CLIENT_NAME", "default-client-name")
API_BASE = os.getenv("VRCHAT_API_BASE", "https://api.vrchat.cloud/api/1")
TOKEN_FILE = Path(os.getenv("TOKEN_FILE", "data/auth/account.json"))
