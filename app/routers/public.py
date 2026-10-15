from fastapi import APIRouter, HTTPException, Request
import json
from app.database import get_db
from app.models import ContactInquiryCreate

router = APIRouter(prefix="/api/public", tags=["Public"])

@router.get("/metadata")
def get_metadata():
    with get_db() as conn:
        row = conn.execute("SELECT * FROM site_metadata LIMIT 1").fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Site metadata not initialized")
        data = dict(row)
        data["metrics"] = json.loads(data["metrics_json"])
        del data["metrics_json"]
        return data

@router.get("/experience")
def get_experience():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM work_history ORDER BY sort_order ASC, id ASC").fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["summary_bullets"] = json.loads(d["summary_bullets"])
            result.append(d)
        return result

@router.get("/projects")
def get_projects(category: str = None):
    with get_db() as conn:
        if category:
            rows = conn.execute("SELECT * FROM projects WHERE category = ? ORDER BY id ASC", (category,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM projects ORDER BY id ASC").fetchall()
            
        result = []
        for r in rows:
            d = dict(r)
            d["tech_stack"] = json.loads(d["tech_stack"])
            result.append(d)
        return result

@router.get("/projects/{slug}")
def get_project_by_slug(slug: str):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM projects WHERE slug = ?", (slug,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Project not found")
        d = dict(row)
        d["tech_stack"] = json.loads(d["tech_stack"])
        return d

@router.post("/contact")
def submit_contact_inquiry(inquiry: ContactInquiryCreate, request: Request):
    if not inquiry.sender_name or not inquiry.sender_email or not inquiry.message:
        raise HTTPException(status_code=400, detail="Missing required contact fields")
        
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contact_inquiries (sender_name, sender_email, subject, message, status)
            VALUES (?, ?, ?, ?, 'new')
        """, (inquiry.sender_name, inquiry.sender_email, inquiry.subject, inquiry.message))
        inquiry_id = cursor.lastrowid
        
    return {
        "status": "success",
        "message": "Thank you for reaching out! Your message has been delivered to Wisdom (contact@wisdomowabor.online) and recorded.",
        "inquiry_id": inquiry_id
    }
