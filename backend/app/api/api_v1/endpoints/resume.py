from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, get_current_user
from app.models.user import User
from app.schemas.skill import UserSkillOut
from app.services.resume_parser import persist_user_skills_from_resume

router = APIRouter()

@router.post("/upload", response_model=List[UserSkillOut])
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    skills = await persist_user_skills_from_resume(file, db, current_user)
    return skills
