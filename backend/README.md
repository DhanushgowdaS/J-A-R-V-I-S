# J-A-R-V-I-S Backend

## Requirements
- Python 3.12+

## Development setup (Windows PowerShell)
```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Endpoints
- `GET /api/health` — service health
- `GET /api` — basic API status

Interactive API docs are available at `http://127.0.0.1:8000/docs` while the backend is running.
