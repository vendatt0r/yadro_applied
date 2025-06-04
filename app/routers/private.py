from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import URLCreate, URLInfo
from app.crud import *
from app.database import SessionLocal
from app.auth import verify_credentials

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=URLInfo)
def create_link(data: URLCreate, db: Session = Depends(get_db), _ = Depends(verify_credentials)):
    return create_url(db, data)

@router.get("/urls", response_model=List[URLInfo])
def list_urls(active: Optional[bool] = Query(None), db: Session = Depends(get_db), _ = Depends(verify_credentials)):
    return get_all_urls(db, active)

@router.post("/deactivate/{code}", response_model=URLInfo)
def deactivate(code: str, db: Session = Depends(get_db), _ = Depends(verify_credentials)):
    url = deactivate_url(db, code)
    if not url:
        raise HTTPException(status_code=404, detail="Not found")
    return url

@router.get("/stats", response_model=List[URLInfo])
def stats(db: Session = Depends(get_db), _ = Depends(verify_credentials)):
    return get_top_urls(db)
