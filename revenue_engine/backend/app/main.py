from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(): return {"status":"ok","service":settings.app_name,"environment":settings.environment}

@app.get("/health/live")
def live(): return {"status":"alive"}

@app.get("/health/ready")
def ready(): return {"status":"ready"}

@app.get("/api/dashboard/metrics")
def metrics(): return {"leads":0,"qualified":0,"contacted":0,"replied":0,"interested":0,"payment_pending":0,"paid":0,"completed":0,"revenue":0}
