from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, get_current_user
from app.models.user import User
from app.models.skill import UserSkill
from app.schemas.user import UserOut, UserUpdate
from app.schemas.skill import UserSkillWithSkill, UserSkillUpdate
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserOut)
def update_users_me(payload: UserUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me/skills", response_model=list[UserSkillWithSkill])
def get_my_skills(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    rows = (
        db.query(UserSkill)
        .options(joinedload(UserSkill.skill))
        .filter(UserSkill.user_id == current_user.id)
        .all()
    )
    return rows

@router.patch("/me/skills/{user_skill_id}", response_model=UserSkillWithSkill)
def update_my_skill(
    user_skill_id: int,
    payload: UserSkillUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    us = (
        db.query(UserSkill)
        .options(joinedload(UserSkill.skill))
        .filter(UserSkill.id == user_skill_id, UserSkill.user_id == current_user.id)
        .first()
    )
    if not us:
        raise HTTPException(status_code=404, detail="UserSkill not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(us, field, value)
    db.add(us)
    db.commit()
    db.refresh(us)
    return us

@router.delete("/me/skills/{user_skill_id}", status_code=204)
def delete_my_skill(
    user_skill_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    us = db.query(UserSkill).filter(UserSkill.id == user_skill_id, UserSkill.user_id == current_user.id).first()
    if not us:
        raise HTTPException(status_code=404, detail="UserSkill not found")
    db.delete(us)
    db.commit()
    return None
