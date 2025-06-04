from __future__ import annotations

import random, string
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app import models, schemas

def generate_short_code(length: int = 6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def create_url(db: Session, data: schemas.URLCreate) -> models.URL:
    db_url = models.URL(
        original_url=str(data.original_url),
        short_code=generate_short_code(),

        is_active=True,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=30),
        visits=0,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_code(db: Session, code: str):
    return db.query(models.URL).filter(models.URL.short_code == code).first()

def get_all_urls(db: Session, active: bool | None = None):
    query = db.query(models.URL)
    if active is not None:
        query = query.filter(models.URL.is_active == active)
    return query.all()

def deactivate_url(db: Session, code: str):
    url = get_url_by_code(db, code)
    if url:
        url.is_active = False
        db.commit()
    return url

def increment_visit(db: Session, url: models.URL):
    url.visits += 1
    db.commit()

def get_top_urls(db: Session):
    return db.query(models.URL).filter(models.URL.is_active == True).order_by(models.URL.visits.desc()).all()
