import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials



load_dotenv()
security = HTTPBasic()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username == ADMIN_USERNAME
    correct_password = credentials.password == ADMIN_PASSWORD
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
