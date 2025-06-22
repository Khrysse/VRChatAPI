<img src="./data/static/logo.png" width="300" style="margin-top: 10px;" draggable="false">

A lightweight, fast, and secure **FastAPI** proxy server for the [VRChat API](https://vrchat.community/getting-started).  
Designed to handle authentication, token management, and provide cached access to public and private VRChat data endpoints.

---

## 🚀 Features

- **Seamless VRChat account authentication** with support for 2FA (email & TOTP)
- Automated token storage and expiry management (configurable cache duration)
- Public API endpoints to fetch VRChat groups & users info
- Private API endpoints secured by VRChat auth tokens
- Written in Python with FastAPI and HTTPX for async requests
- Auto environment setup with virtual environment creation & dependency installation
- Ready to deploy on any server with Python 3.8+ (tested with YunoHost)

---

## 💡 Why this project?

VRChat’s official API requires complex login flows and token management that can be cumbersome to implement for your apps or bots.  
**K-API** simplifies this by handling authentication and caching internally, exposing easy REST endpoints for your applications.

---

## 🛠️ Getting Started

### Requirements

- Python 3.8 or higher installed globally
- Git (optional)

### Installation & Running

Clone this repository:

```bash
git clone https://git.kvs.fyi/kryscau/VRChatAPI.git
# You can use the mirror with Github with: https://github.com/kryscau/VRChatAPI.git
cd VRChatAPI
```

Run the included Python bootstrap script to create and activate the virtual environment, install dependencies, authenticate your VRChat account, and start the server:

```bash
python run.py
```

> This script will prompt for your VRChat username, password, and 2FA code if required.  
> Tokens are stored securely and refreshed automatically every 30 days.

### Access the API

- Public endpoint example:  
  `GET /api/public/groups/{group_id}`  
  Returns info about a VRChat group.

- Private endpoint example (requires authentication or specific permission in VRChat [join group, bans perms, ...]):  
  `GET /api/private/users/{user_id}`  
  Returns private user data accessible with your token.

Explore interactive docs at:  
`http://127.0.0.1:8000/docs`

---

## 🔒 Security & Privacy

- Your VRChat credentials and tokens are stored **locally** in JSON files inside the `data/auth/` directory.
- No credentials or tokens are ever sent to third-party servers.
- Use HTTPS and proper firewall rules when deploying publicly.

---

## 📁 Project Structure

```
/app
    /api           # FastAPI route modules (public/private)
/data/auth        # Token storage (auto-generated)
/prelaunch        # Authentication helper scripts
run.py            # Python bootstrapper script
requirements.txt  # Python dependencies
README.md         # This file
```

---

## 🤝 Contribution

Feel free to open issues or submit pull requests.  
Feature requests and bug reports are welcome!

---

## ⚡ License

MIT License © 2025 Kryscau (K-API)

---

## 🚀 Next Steps

- Add WebSocket support for real-time VRChat events
- Implement caching layers with Redis or similar
- Dockerize for easy container deployments
- Add OAuth support for multi-user API proxies

---

Made with ❤️ by [Kryscau](https://kryscau.github.io).
