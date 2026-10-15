from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Any, Dict

class SiteMetadataModel(BaseModel):
    id: Optional[int] = None
    full_name: str
    professional_headline: str
    bio: str
    contact_email: str
    phone: str
    location: str
    metrics: Dict[str, Any]

class WorkHistoryModel(BaseModel):
    id: Optional[int] = None
    company: str
    role_title: str
    period: str
    location: str
    summary_bullets: List[str]
    sort_order: int = 0

class ProjectModel(BaseModel):
    id: Optional[int] = None
    slug: str
    title: str
    category: str
    summary: str
    architecture_breakdown: str
    tech_stack: List[str]
    github_url: str
    live_status: int = 1
    sandbox_route: str

class ContactInquiryCreate(BaseModel):
    sender_name: str
    sender_email: str
    subject: str
    message: str

class ContactInquiryModel(BaseModel):
    id: int
    sender_name: str
    sender_email: str
    subject: str
    message: str
    status: str
    timestamp: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminUserResponse(BaseModel):
    id: int
    username: str
    role: str
