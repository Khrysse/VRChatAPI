import os
import sys
import subprocess
import venv
import time
import json
from pathlib import Path

VENV_DIR = "venv"
REQ_FILE = "requirements.txt"
TOKEN_FILE = Path("data/auth/account.json")

# Ajout PYTHONPATH pour que 'app' soit trouvé dans les subprocess
project_root = os.path.abspath(os.path.dirname(__file__))
os.environ["PYTHONPATH"] = project_root + os.pathsep + os.environ.get("PYTHONPATH", "")
port = os.environ.get("PORT", "8080")

def create_venv():
    print("Creating virtual environment...", flush=True)
    venv.create(VENV_DIR, with_pip=True)

def run_in_venv(cmd, env=None):
    if os.name == "nt":
        python_bin = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        python_bin = os.path.join(VENV_DIR, "bin", "python")
    full_cmd = [python_bin] + cmd
    result = subprocess.run(full_cmd, env=env)
    if result.returncode != 0:
        print(f"Command {cmd} failed.", flush=True)
        sys.exit(result.returncode)

def install_requirements():
    print("Installing dependencies...", flush=True)
    run_in_venv(["-m", "pip", "install", "--upgrade", "pip"])
    run_in_venv(["-m", "pip", "install", "-r", REQ_FILE])

def is_token_valid():
    if not TOKEN_FILE.exists():
        print("Token file does not exist.", flush=True)
        return False
    try:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
        if "auth_cookie" not in data:
            print("Token file missing auth_cookie.", flush=True)
            return False
        if "created_at" not in data:
            print("Token file missing created_at.", flush=True)
            return False
        from datetime import datetime, timezone, timedelta
        created = datetime.fromisoformat(data["created_at"])
        if datetime.now(timezone.utc) - created > timedelta(days=30):
            print("Token expired.", flush=True)
            return False
        return True
    except Exception as e:
        print("Error reading token file:", e, flush=True)
        return False

def main():
    if not os.path.exists(VENV_DIR):
        create_venv()
        install_requirements()
    else:
        print("Virtual environment found.", flush=True)

    # S'assurer que le fichier token existe (même vide)
    if not TOKEN_FILE.exists():
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text("{}")

    env = os.environ.copy()
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

    if is_token_valid():
        print("Valid token found, launching server normally.", flush=True)
        run_in_venv([
            "-m", "uvicorn", "app.main:app",
            "--host", "0.0.0.0", "--port", port, "--reload"
        ], env=env)
    else:
        print("No valid token found, launching auth mode (server + login)...", flush=True)

        if os.name == "nt":
            python_bin = os.path.join(VENV_DIR, "Scripts", "python.exe")
        else:
            python_bin = os.path.join(VENV_DIR, "bin", "python")

        auth_server_cmd = [python_bin, "app/main.py", "--auth-mode"]
        print("Starting auth-mode server...", flush=True)
        auth_server_proc = subprocess.Popen(auth_server_cmd, env=env)

        try:
            time.sleep(2)
            print("Running VRChat authentication script (login)...", flush=True)
            login_cmd = [python_bin, "python/vrchat_auth.py"]
            login_proc = subprocess.run(login_cmd, env=env)

            if not is_token_valid():
                print("❌ Token file still not valid after login. Exiting.", flush=True)
                auth_server_proc.terminate()
                try:
                    auth_server_proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print("Auth server did not stop, killing...", flush=True)
                    auth_server_proc.kill()
                sys.exit(1)

            print("✅ Login successful, stopping auth-mode server...", flush=True)
            auth_server_proc.terminate()
            try:
                auth_server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Auth server did not stop, killing...", flush=True)
                auth_server_proc.kill()

            print("Starting main FastAPI server...", flush=True)
            subprocess.run([
                python_bin, "-m", "uvicorn", "app.main:app",
                "--host", "0.0.0.0", "--port", port, "--reload"
            ], env=env)
        except Exception as e:
            print(f"Unexpected error during authentication: {e}", flush=True)
            auth_server_proc.terminate()
            try:
                auth_server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                auth_server_proc.kill()
            sys.exit(1)

if __name__ == "__main__":
    main()