from typing import Optional
from pydantic import BaseModel, EmailStr
from beanie import Document

class TokenAuth(BaseModel):
    access_token: str
    refresh_token: str

class UserInfo(Document, BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    email: EmailStr
    password: str

    class Settings:
        name = 'user_info'
