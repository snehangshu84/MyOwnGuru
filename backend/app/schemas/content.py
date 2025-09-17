from typing import Optional, List, Any
from pydantic import BaseModel

class ContentBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    content_type: str
    provider: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_hours: Optional[float] = None
    language: Optional[str] = "en"

class ContentOut(ContentBase):
    id: int

    class Config:
        from_attributes = True

class ContentRecommendationOut(BaseModel):
    id: int
    user_id: int
    content_id: int
    recommendation_score: float
    recommendation_reason: Optional[str] = None

    class Config:
        from_attributes = True
