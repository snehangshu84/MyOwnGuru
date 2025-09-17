from typing import Optional, List
from pydantic import BaseModel

class SkillBase(BaseModel):
    name: str
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None

class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True

class UserSkillBase(BaseModel):
    skill_id: int
    proficiency_level: float
    confidence_level: Optional[float] = None
    years_of_experience: Optional[float] = None
    source: Optional[str] = None
    evidence: Optional[str] = None
    is_learning_goal: Optional[bool] = False
    target_proficiency: Optional[float] = None
    priority: Optional[str] = "medium"

class UserSkillOut(UserSkillBase):
    id: int

    class Config:
        from_attributes = True

class UserSkillWithSkill(UserSkillOut):
    skill: SkillOut

    class Config:
        from_attributes = True

class UserSkillUpdate(BaseModel):
    proficiency_level: Optional[float] = None
    confidence_level: Optional[float] = None
    years_of_experience: Optional[float] = None
    is_learning_goal: Optional[bool] = None
    target_proficiency: Optional[float] = None
    priority: Optional[str] = None
    evidence: Optional[str] = None
