import os, webbrowser
import uvicorn

os.environ.setdefault("OUTREACH_DRY_RUN", "true")
print("Starting Amravati Revenue Engine in safe local mode...")
webbrowser.open("http://127.0.0.1:8000/docs")
uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
