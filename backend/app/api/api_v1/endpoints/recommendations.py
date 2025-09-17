from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, get_current_user
from app.models.user import User
from app.schemas.content import ContentRecommendationOut
from app.services.recommender import get_recommendations

router = APIRouter()

@router.get("/content", response_model=List[ContentRecommendationOut])
async def content_recommendations(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    recs = await get_recommendations(current_user)
    return recs
