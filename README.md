<center>
<img src="https://cdn.unstealable.cloud/vrchat-bridge/images/logo.min.png" alt="VRChat Bridge (Min Logo)" width="150">

# VRChat Bridge API

A lightweight, fast, and secure **FastAPI** proxy server for the [VRChat API](https://vrchat.community/getting-started).  
Designed to handle authentication, token management, and provide cached access to public and private VRChat data endpoints.

</center>

---

## 🚀 Features

### Core Features

- **Seamless VRChat account authentication** with support for 2FA (email & TOTP)
- **Automated token storage and expiry management** (configurable cache duration)
- **Public API endpoints** to fetch VRChat groups & users info
- **Private API endpoints** secured by VRChat auth tokens
- **Web-based authentication interface** for easy token management
- **Docker support** with automated builds and deployments
- **GitHub Actions workflow** for automated Docker Hub pushes

### API Endpoints

- **Users API**: Search, fetch user details, and manage user data
- **Groups API**: Group information, members, and management
- **Worlds API**: World details and information
- **Avatars API**: Avatar data and management
- **Search API**: Advanced search functionality across VRChat
- **System API**: Health checks and system status
- **Webhook Auth API**: Authentication webhook endpoints

### Technical Features

- **Written in Python** with FastAPI and HTTPX for async requests
- **Auto environment setup** with virtual environment creation & dependency installation
- **Ready to deploy** on any server with Python 3.8+ (tested with YunoHost)
- **Docker containerization** for easy deployment
- **Apache + PHP** frontend with URL rewriting support
- **Supervisor** for process management
- **Python-based scheduled tasks** for automated operations

---

## 🛠️ Getting Started

### Requirements

- Python 3.8 or higher installed globally
- Git (optional)
- Docker (optional, for containerized deployment)

### Installation & Running

#### Method 1: Direct Python Installation

Clone this repository:

```bash
git clone https://github.com/unstealable/VRChatBridge.git
cd VRChatBridge
```

Run the included Python bootstrap script to create and activate the virtual environment, install dependencies, authenticate your VRChat account, and start the server:

```bash
python run.py
```

> This script will prompt for your VRChat username, password, and 2FA code if required.  
> Tokens are stored securely and refreshed automatically every 30 days.

#### Method 2: Docker Deployment

Build and run with Docker:

```bash
# Build the image
docker build -t unstealable/vrchatbridge:latest .

# Run the container
docker run -p 8080:8080 -p 80:80 unstealable/vrchatbridge:latest
```

Or use Docker Compose:

```bash
docker-compose up -d
```

#### Method 3: Automated Docker Hub Deployment

Use the included GitHub Actions workflow to automatically build and push to Docker Hub:

1. Configure GitHub Secrets (`DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`)
2. Go to Actions tab in your repository
3. Run the "Build and Push Docker Image" workflow
4. Pull the image: `docker pull unstealable/vrchatbridge:latest`

### Access the API

- **API Documentation**: `http://127.0.0.1:8080/docs`
- **Web Interface**: `http://127.0.0.1:80` (main interface)
- **Health Check**: `http://127.0.0.1:8080/api/health`

#### Example API Calls

**Public endpoint example**:  
`GET /api/public/groups/{group_id}`  
Returns info about a VRChat group.

**Private endpoint example** (requires authentication):  
`GET /api/private/users/{user_id}`  
Returns private user data accessible with your token.

---

## 📁 Project Structure

```
VRChatAPI/
├── app/                    # FastAPI application
│   ├── api/               # API route modules
│   │   ├── system.py      # System endpoints
│   │   ├── vrchat_users.py    # User management
│   │   ├── vrchat_groups.py   # Group management
│   │   ├── vrchat_worlds.py   # World data
│   │   ├── vrchat_avatars.py  # Avatar management
│   │   ├── vrchat_search.py   # Search functionality
│   │   └── webhook_auth.py    # Authentication webhooks
│   ├── main.py            # FastAPI app creation
│   ├── env.py             # Environment configuration
│   └── vrchat_context.py  # VRChat context management
├── php/                   # Web interface
│   ├── api/               # PHP API endpoints
│   ├── assets/            # CSS/JS assets
│   └── index.php          # Main interface
├── python/                # Python utilities
├── .github/workflows/     # GitHub Actions
│   ├── docker-push.yml    # Docker build workflow
│   └── README.md          # Workflow documentation
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── requirements.txt       # Python dependencies
├── supervisord.conf      # Process management
├── apache-config.conf    # Apache configuration
├── entrypoint.sh         # Container entrypoint
├── run.py                # Python bootstrap script
└── app/cron_checker.py   # Scheduled tasks
```

---

## 🔧 Configuration

### Environment Variables

| Variable               | Description              | Default                          |
| ---------------------- | ------------------------ | -------------------------------- |
| `PORT`                 | API server port          | `8080`                           |
| `APACHE_PORT`          | Apache web server port   | `80`                             |
| `API_IS_PUBLIC`        | Enable public API access | `true`                           |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins     | `*`                              |
| `CLIENT_NAME`          | VRChat client name       | `default-client-name`            |
| `VRCHAT_API_BASE`      | VRChat API base URL      | `https://api.vrchat.cloud/api/1` |
| `TOKEN_FILE`           | Token storage file path  | `data/auth/account.json`         |
| `IS_DISTANT`           | Enable distant mode      | `false`                          |
| `DISTANT_URL_CONTEXT`  | Distant URL context      | `""`                             |

### Docker Configuration

The project includes:

- **Dockerfile**: Multi-stage build with Python and Apache
- **docker-compose.yml**: Complete service orchestration
- **supervisord.conf**: Process management for multiple services
- **entrypoint.sh**: Container initialization script

### GitHub Actions

Automated workflow for Docker Hub deployment:

- Manual trigger with custom tags
- Multi-architecture support
- Cached builds for performance
- Automatic push to Docker Hub

---

## 🔒 Security & Privacy

- Your VRChat credentials and tokens are stored **locally** in JSON files inside the `data/auth/` directory
- No credentials or tokens are ever sent to third-party servers
- Use HTTPS and proper firewall rules when deploying publicly
- Web interface provides secure authentication flow
- All API endpoints include proper error handling and validation

---

## 🌐 Web Interface

The project includes a PHP-based web interface for:

- **Authentication management**: Login/logout with VRChat credentials
- **2FA handling**: Secure two-factor authentication
- **Status monitoring**: Real-time connection status
- **User-friendly interface**: Modern, responsive design

Access via: `http://your-domain/` or `http://localhost/`

---

## 🚀 Deployment Options

### 1. Local Development

```bash
python run.py
```

### 2. Docker Container

```bash
docker run -p 8080:8080 -p 80:80 unstealable/vrchatbridge:latest
```

### 3. Docker Compose

```bash
docker-compose up -d
```

### 4. Production Server

- Deploy with Apache/Nginx reverse proxy
- Use environment variables for configuration
- Enable HTTPS with SSL certificates
- Set up proper firewall rules

---

## 📊 API Endpoints Overview

### Public Endpoints

- `GET /api/health` - Health check
- `GET /api/public/groups/{group_id}` - Group information
- `GET /api/public/users/{user_id}` - Public user data

### Private Endpoints (Require Authentication)

- `GET /api/private/users/{user_id}` - Private user data
- `GET /api/private/groups/{group_id}` - Private group data
- `POST /api/search/users` - User search
- `POST /api/search/worlds` - World search

### Webhook Endpoints

- `POST /webhook/auth/login` - Authentication login
- `POST /webhook/auth/2fa` - Two-factor authentication
- `GET /webhook/auth/status` - Authentication status

---

## 🤝 Contribution

Feel free to open issues or submit pull requests.  
Feature requests and bug reports are welcome!

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License © 2025 Kryscau (K-API)

---

## 🚀 Roadmap

- [ ] Add WebSocket support for real-time VRChat events
- [ ] Implement caching layers with Redis or similar
- [ ] Add OAuth support for multi-user API proxies
- [ ] Enhanced monitoring and logging
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline improvements

---

Made with ❤️ by [Unstealable](https://unstealable.github.io).
