from fastapi import FastAPI
from app.routers import public, private
from app.database import create_db

app = FastAPI(title="URL Service")

create_db()

app.include_router(public.router)
app.include_router(private.router, prefix="/admin")
