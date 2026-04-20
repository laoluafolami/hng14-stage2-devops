# HNG14 Stage 2 DevOps — Job Processing System

A containerised job processing system with a Node.js frontend, Python/FastAPI backend, Python worker, and Redis queue.

## Architecture

[Browser] → [Frontend :3000] → [API :8000] → [Redis] ↑ [Worker]

## Prerequisites

Install the following on your machine:

- [Docker](https://docs.docker.com/get-docker/) (v24+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.20+)
- Git

Verify installations:

```bash
docker --version
docker compose version
git --version
```

## Quick Start (Bring Up on a Clean Machine)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hng14-stage2-devops.git
cd hng14-stage2-devops
```

### 2. Create your .env file

```bash
cp .env.example .env
```

Open `.env` and set a secure password:

```env
REDIS_PASSWORD=your_secure_password_here
APP_ENV=production
```

### 3. Build and start all services

```bash
docker compose up --build -d
```

### 4. Verify all services are healthy

```bash
docker compose ps
```

Expected output shows all services as `healthy`:

```
NAME         STATUS              PORTS
redis        Up (healthy)
api          Up (healthy)        0.0.0.0:8000->8000/tcp
worker       Up (healthy)
frontend     Up (healthy)        0.0.0.0:3000->3000/tcp
```

### 5. Open the application

Visit: http://localhost:3000

Click **Submit New Job** — you will see a job ID appear and its status update from `queued` → `completed` within a few seconds.

## What a Successful Startup Looks Like
```
✔ Container redis    Healthy
✔ Container api      Healthy
✔ Container worker   Started
✔ Container frontend Healthy
```
The frontend is accessible at http://localhost:3000  
The API is accessible at http://localhost:8000/docs

## Running Tests Locally

```bash
cd api
pip install -r requirements.txt
pytest --cov=. --cov-report=term-missing
```

## Stopping the Stack

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down -v
```

## CI/CD Pipeline

The GitHub Actions pipeline at `.github/workflows/ci-cd.yml` runs automatically on every push:

| Stage | Description |
|---|---|
| lint | flake8 (Python), eslint (JS), hadolint (Dockerfiles) |
| test | pytest with mocked Redis, uploads coverage artifact |
| build | Builds and pushes all 3 images to a local registry |
| security-scan | Trivy scans all images; fails on CRITICAL findings |
| integration-test | Brings full stack up, submits job, asserts completion |
| deploy | Rolling update on pushes to `main` only |

## Environment Variables

See `.env.example` for all required variables.