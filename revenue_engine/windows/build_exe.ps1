$ErrorActionPreference = "Stop"
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r ..\backend\requirements.txt pyinstaller
pyinstaller --onefile --name AmravatiRevenueEngine launcher.py
Write-Host "EXE created under dist\AmravatiRevenueEngine.exe"
