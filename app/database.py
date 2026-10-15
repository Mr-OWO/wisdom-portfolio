import sqlite3
import json
from contextlib import contextmanager
from app.config import DATABASE_PATH

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_db():
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. admin_users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'SuperAdmin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # 2. site_metadata
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            professional_headline TEXT NOT NULL,
            bio TEXT NOT NULL,
            contact_email TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            metrics_json TEXT NOT NULL,
            profile_image_url TEXT DEFAULT '/static/img/wisdom_avatar.jpg'
        );
        """)
        
        # 3. work_history
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role_title TEXT NOT NULL,
            period TEXT NOT NULL,
            location TEXT NOT NULL,
            summary_bullets TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        """)
        
        # 4. projects
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            summary TEXT NOT NULL,
            architecture_breakdown TEXT NOT NULL,
            tech_stack TEXT NOT NULL,
            github_url TEXT NOT NULL,
            live_status INTEGER NOT NULL DEFAULT 1,
            sandbox_route TEXT NOT NULL
        );
        """)
        
        # 5. contact_inquiries
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT NOT NULL,
            sender_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'new',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # 6. audit_logs (for RBAC & Security tracking)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor TEXT NOT NULL,
            action TEXT NOT NULL,
            resource TEXT NOT NULL,
            status TEXT NOT NULL,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Add index for project slug lookups
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_slug ON projects(slug);")
