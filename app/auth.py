import bcrypt
import hmac
import hashlib
import time
import base64
import json
from typing import Optional
from fastapi import Request, HTTPException, Depends
from app.config import SECRET_KEY, SESSION_COOKIE_NAME
from app.database import get_db

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def generate_session_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + (86400 * 7) # 7 days
    }
    payload_bytes = json.dumps(payload).encode("utf-8")
    sig = hmac.new(SECRET_KEY.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
    token = base64.urlsafe_b64encode(payload_bytes).decode("utf-8") + "." + sig
    return token

def verify_session_token(token: str) -> Optional[dict]:
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        payload_b64, sig = parts
        payload_bytes = base64.urlsafe_b64decode(payload_b64.encode("utf-8"))
        expected_sig = hmac.new(SECRET_KEY.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        payload = json.loads(payload_bytes.decode("utf-8"))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None

def get_current_admin(request: Request) -> dict:
    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    auth_header = request.headers.get("Authorization")
    token = None
    if session_cookie:
        token = session_cookie
    elif auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")
        
    admin_payload = verify_session_token(token)
    if not admin_payload:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
        
    with get_db() as conn:
        user = conn.execute("SELECT id, username, role FROM admin_users WHERE username = ?", (admin_payload["sub"],)).fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Admin user no longer exists")
        return dict(user)
