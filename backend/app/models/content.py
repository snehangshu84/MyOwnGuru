"""
Content models for learning resources and recommendations
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Content identification
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    url = Column(String, nullable=False)
    content_type = Column(String, nullable=False)  # course, tutorial, video, article, book, project
    
    # Provider information
    provider = Column(String)  # coursera, udemy, youtube, medium, github, etc.
    author = Column(String)
    instructor = Column(String)
    
    # Content characteristics
    difficulty_level = Column(String)  # beginner, intermediate, advanced, expert
    duration_hours = Column(Float)
    language = Column(String, default="en")
    format = Column(String)  # video, text, interactive, hands-on, etc.
    
    # Quality metrics
    rating = Column(Float)  # 0-5 scale
    review_count = Column(Integer, default=0)
    popularity_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)  # AI-assessed quality
    
    # Content metadata
    tags = Column(JSON)  # List of relevant tags
    skills_covered = Column(JSON)  # List of skills this content covers
    prerequisites = Column(JSON)  # Required skills or knowledge
    learning_outcomes = Column(JSON)  # What learners will achieve
    
    # Pricing and access
    is_free = Column(Boolean, default=True)
    price = Column(Float)
    currency = Column(String, default="USD")
    requires_subscription = Column(Boolean, default=False)
    
    # Content status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_updated = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recommendations = relationship("ContentRecommendation", back_populates="content")
    
    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', provider='{self.provider}')>"

class ContentRecommendation(Base):
    __tablename__ = "content_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    
    # Recommendation metadata
    recommendation_score = Column(Float, nullable=False)  # 0-100 scale
    recommendation_reason = Column(Text)
    recommendation_type = Column(String)  # skill_gap, career_goal, trending, peer_recommended
    
    # Personalization factors
    skill_relevance_score = Column(Float)
    career_alignment_score = Column(Float)
    difficulty_match_score = Column(Float)
    learning_style_match_score = Column(Float)
    
    # User interaction
    status = Column(String, default="recommended")  # recommended, viewed, bookmarked, started, completed, dismissed
    user_rating = Column(Float)
    user_feedback = Column(Text)
    
    # Context
    recommended_for_skill = Column(String)
    recommended_in_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    viewed_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    content = relationship("Content", back_populates="recommendations")
    
    def __repr__(self):
        return f"<ContentRecommendation(id={self.id}, user_id={self.user_id}, content_id={self.content_id}, score={self.recommendation_score})>"
