import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import public, admin, labs

app = FastAPI(
    title="Wisdom Ogechi Owabor - Portfolio & Enterprise SecOps Hub",
    description="Principal Full-Stack, Cybersecurity & Technical Support Portfolio System",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Include Routers
app.include_router(public.router)
app.include_router(admin.router)
app.include_router(labs.router)

@app.on_event("startup")
def on_startup():
    init_db()

# Multi-Page Route Handlers
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse(TEMPLATES_DIR / "index.html")

@app.get("/about", response_class=HTMLResponse)
async def serve_about():
    return FileResponse(TEMPLATES_DIR / "about.html")

@app.get("/projects", response_class=HTMLResponse)
async def serve_projects():
    return FileResponse(TEMPLATES_DIR / "projects.html")

@app.get("/projects/{slug}", response_class=HTMLResponse)
async def serve_project_slug(slug: str):
    return FileResponse(TEMPLATES_DIR / "projects.html")

@app.get("/contact", response_class=HTMLResponse)
async def serve_contact():
    return FileResponse(TEMPLATES_DIR / "contact.html")

@app.get("/admin", response_class=HTMLResponse)
@app.get("/admin/{rest_of_path:path}", response_class=HTMLResponse)
async def serve_admin():
    return FileResponse(TEMPLATES_DIR / "admin.html")
