from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    job_title: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    experience_level: Optional[str] = None
    career_goals: Optional[str] = None
    preferred_learning_style: Optional[str] = None
    linkedin_profile: Optional[str] = None
    github_profile: Optional[str] = None
    portfolio_url: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    experience_level: Optional[str] = None
    career_goals: Optional[str] = None
    preferred_learning_style: Optional[str] = None
    linkedin_profile: Optional[str] = None
    github_profile: Optional[str] = None
    portfolio_url: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
