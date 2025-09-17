from typing import Optional, Any
from pydantic import BaseModel

class ProgressOut(BaseModel):
    id: int
    user_id: int
    progress_type: str
    progress_percentage: float

    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    feedback_type: str
    rating: Optional[float] = None
    title: Optional[str] = None
    comment: Optional[str] = None
    is_anonymous: Optional[bool] = False
