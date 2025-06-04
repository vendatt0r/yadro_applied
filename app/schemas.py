from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl
    expires_in_days: int = 1

class URLInfo(BaseModel):
    short_code: str
    original_url: str
    is_active: bool
    created_at: datetime
    expires_at: datetime
    visits: int

    class Config:
        orm_mode = True
