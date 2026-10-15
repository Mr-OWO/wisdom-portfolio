import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "portfolio.db"))
SECRET_KEY = os.getenv("SECRET_KEY", "wisdom-portfolio-cyber-secops-key-2026-production-token")
ALGORITHM = "HS256"
SESSION_COOKIE_NAME = "wisdom_admin_session"

# GitHub API credentials
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "Mr-OWO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
