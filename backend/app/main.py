from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="J-A-R-V-I-S API",
    version="0.1.0",
    description="Local API foundation for the J-A-R-V-I-S personal assistant.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/api/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Basic service health endpoint."""
    return {"status": "ok", "service": "J-A-R-V-I-S API", "version": "0.1.0"}

@app.get("/api", tags=["system"])
def api_info() -> dict[str, str]:
    return {"name": "J-A-R-V-I-S", "status": "foundation", "message": "Backend is running."}
