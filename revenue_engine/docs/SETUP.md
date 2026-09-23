# Complete Setup Guide

## Local development
1. Install Python 3.12+ and Node.js 20+.
2. Copy the example environment file to .env and set a strong SECRET_KEY.
3. Create a Python virtual environment.
4. Install backend requirements.
5. Run uvicorn app.main:app --reload --port 8000 from the backend directory.
6. Open /docs for the API.

## Docker
From the revenue_engine directory run: docker compose up --build.

## Windows EXE
Run windows/build_exe.ps1. The generated EXE starts the local API in safe dry-run mode. Production credentials must be supplied externally.

## Production
Use PostgreSQL, Redis, HTTPS, secret management, backups, provider webhooks, monitoring and a separate worker process. Never place real credentials in Git.
