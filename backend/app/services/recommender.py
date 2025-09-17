from typing import List
from app.schemas.content import ContentRecommendationOut
from app.models.user import User

async def get_recommendations(user: User) -> List[ContentRecommendationOut]:
    # TODO: implement real recommender using content aggregation and skill gaps
    return [
        ContentRecommendationOut(id=1, user_id=user.id, content_id=1001, recommendation_score=92.5, recommendation_reason="Matches your target skill: Data Engineering"),
        ContentRecommendationOut(id=2, user_id=user.id, content_id=1002, recommendation_score=88.0, recommendation_reason="Beginner-friendly course aligned with your goals"),
    ]
