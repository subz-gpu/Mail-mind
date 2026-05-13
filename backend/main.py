import sys
import os

# Add backend folder to path so all imports resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.emails import router as email_router

app = FastAPI(
    title="Email Reply Generator",
    description="AI-powered email reply generator using Gmail + Gemini",
    version="1.0.0"
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(email_router, prefix="/api")

# Serve frontend — path relative to project root
frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_frontend():
    index = os.path.join(frontend_path, "index.html")
    return FileResponse(index)

@app.get("/health")
def health():
    return {"status": "ok", "message": "Email Reply Generator is running"}