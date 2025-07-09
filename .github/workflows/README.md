# Docker Hub Push Workflow

This workflow allows you to automatically build and push Docker images to Docker Hub.

## Required Configuration

### 1. GitHub Secrets

You need to configure the following secrets in your GitHub repository:

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:

#### `DOCKERHUB_USERNAME`

- Your Docker Hub username
- Example: `unstealable`

#### `DOCKERHUB_TOKEN`

- Your Docker Hub access token (not your password)
- To create a token:
  1. Log in to [Docker Hub](https://hub.docker.com)
  2. Go to **Account Settings** → **Security**
  3. Click on **New Access Token**
  4. Give the token a name (e.g., "GitHub Actions")
  5. Copy the generated token

## Usage

### Manual Trigger

1. Go to the **Actions** tab of your GitHub repository
2. Select the **"Build and Push Docker Image"** workflow
3. Click on **"Run workflow"**
4. Enter the desired tag (e.g., `latest`, `v1.0.0`, `v2.1.3`)
5. Click on **"Run workflow"**

### Recommended Tags

- `latest` : Most recent version
- `v1.0.0` : Specific version (semantic versioning)
- `dev` : Development version
- `stable` : Stable version

## Features

- ✅ Automatic Docker image build
- ✅ Push to Docker Hub with specified tag
- ✅ Docker cache for faster builds
- ✅ Success notifications
- ✅ Multi-architecture support (via Docker Buildx)

## Equivalent Docker Commands

The workflow automatically does what you would do manually:

```bash
# Build the image
docker build -t unstealable/vrchatbridge:latest .

# Push to Docker Hub
docker push unstealable/vrchatbridge:latest
```

## Verification

After running the workflow, you can verify that your image has been pushed:

1. Visit your Docker Hub page: https://hub.docker.com/r/unstealable/vrchatbridge
2. Check that the new tag appears in the list
3. Test the pull: `docker pull unstealable/vrchatbridge:latest`
