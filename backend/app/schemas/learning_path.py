from typing import Optional, List, Any
from pydantic import BaseModel

class LearningPathStepBase(BaseModel):
    title: str
    description: Optional[str] = None
    step_number: int
    step_type: Optional[str] = None
    content_url: Optional[str] = None
    content_provider: Optional[str] = None
    estimated_duration_hours: Optional[float] = None
    prerequisites: Optional[Any] = None
    dependencies: Optional[Any] = None

class LearningPathStepOut(LearningPathStepBase):
    id: int

    class Config:
        from_attributes = True

class LearningPathStepUpdate(BaseModel):
    status: Optional[str] = None  # not_started, in_progress, completed, skipped
    progress_percentage: Optional[float] = None

class LearningPathBase(BaseModel):
    title: str
    description: Optional[str] = None
    goal: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_duration_weeks: Optional[int] = None
    category: Optional[str] = None

class LearningPathOut(LearningPathBase):
    id: int
    progress_percentage: float

    class Config:
        from_attributes = True

class LearningPathWithSteps(LearningPathOut):
    steps: List[LearningPathStepOut] = []

    class Config:
        from_attributes = True
