from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

CLIENT_NAME = os.getenv("CLIENT_NAME", "default-client-name")
API_BASE = os.getenv("VRCHAT_API_BASE", "https://api.vrchat.cloud/api/1")
TOKEN_FILE = Path(os.getenv("TOKEN_FILE", "data/auth/account.json"))
IS_RENDER = os.getenv("IS_RENDER", "false").lower() in ("true", "1", "t")
ACCOUNT_URL_JSON = os.getenv("ACCOUNT_JSON_URL", "https://example.com/vrcapi_render_download_acc.php")
ACCOUNT_JSON_TOKEN = os.getenv("ACCOUNT_JSON_TOKEN", "your-token-here")