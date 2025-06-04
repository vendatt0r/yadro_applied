from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.crud import get_url_by_code, increment_visit

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    url = get_url_by_code(db, short_code)
    if not url or not url.is_active or url.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Link expired or not found")
    increment_visit(db, url)
    return RedirectResponse(url.original_url)
