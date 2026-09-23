import os, sys, webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
os.environ.setdefault("OUTREACH_DRY_RUN", "true")

import uvicorn

print("Starting Amravati Revenue Engine in safe local mode...")
webbrowser.open("http://127.0.0.1:8000/docs")
uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
