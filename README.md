# J-A-R-V-I-S

Private, independently developed personal AI assistant project.

## Quick demo (Windows)
1. Install Python 3.12 and Node.js 20+.
2. Download/clone this private repository.
3. Double-click START-JARVIS-DEMO.bat.
4. The launcher installs/checks dependencies, starts backend and frontend, then opens the browser demo.

Keep both terminal windows open. UI: http://127.0.0.1:5173; API: http://127.0.0.1:8000.

## Demo features
- Neural-network visual interface
- Chat and saved conversations
- Settings
- Browser-dependent voice input/output
- Local SQLite storage and persistent memory
- Allowlisted calculator and UTC time tools

AI replies require provider setup in backend/.env using backend/.env.example. Without a key, setup-mode replies clearly explain that AI is not configured.

## Manual setup
Backend (Python 3.12+):
```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Frontend:
```powershell
cd frontend
npm install
npm run dev
```

## Security
Provider keys stay in backend environment. Arbitrary shell/code execution is not exposed. Local DB data is git-ignored.

Project is an active demo foundation; full integrations and desktop packaging are not complete yet.
