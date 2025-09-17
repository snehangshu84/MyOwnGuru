"""
Progress and feedback models for tracking learning journey
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Progress tracking
    content_id = Column(Integer, ForeignKey("content.id"))
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    learning_path_step_id = Column(Integer, ForeignKey("learning_path_steps.id"))
    
    # Progress details
    progress_type = Column(String, nullable=False)  # content, path, step, skill, overall
    progress_percentage = Column(Float, default=0.0)
    status = Column(String)  # not_started, in_progress, completed, paused, abandoned
    
    # Time tracking
    time_spent_minutes = Column(Integer, default=0)
    sessions_count = Column(Integer, default=0)
    
    # Performance metrics
    completion_rate = Column(Float)
    accuracy_score = Column(Float)  # For assessments
    engagement_score = Column(Float)  # AI-calculated engagement
    
    # Learning analytics
    learning_velocity = Column(Float)  # Progress per unit time
    difficulty_rating = Column(Float)  # User's perceived difficulty
    effectiveness_rating = Column(Float)  # How effective the learning was
    
    # Milestones and achievements
    milestones_reached = Column(JSON)
    badges_earned = Column(JSON)
    certificates_earned = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    last_activity = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="progress")
    
    def __repr__(self):
        return f"<Progress(id={self.id}, user_id={self.user_id}, type='{self.progress_type}', progress={self.progress_percentage}%)>"

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Feedback context
    feedback_type = Column(String, nullable=False)  # content, path, step, platform, recommendation
    content_id = Column(Integer, ForeignKey("content.id"))
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    learning_path_step_id = Column(Integer, ForeignKey("learning_path_steps.id"))
    
    # Feedback content
    rating = Column(Float)  # 1-5 scale
    title = Column(String)
    comment = Column(Text)
    
    # Specific feedback dimensions
    content_quality_rating = Column(Float)
    difficulty_rating = Column(Float)
    relevance_rating = Column(Float)
    engagement_rating = Column(Float)
    
    # Feedback categories
    is_positive = Column(Boolean)
    is_constructive = Column(Boolean, default=True)
    sentiment_score = Column(Float)  # AI-analyzed sentiment
    
    # Feedback metadata
    is_anonymous = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    helpfulness_score = Column(Float, default=0.0)
    
    # Response and resolution
    response_from_provider = Column(Text)
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    responded_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="feedback")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, user_id={self.user_id}, type='{self.feedback_type}', rating={self.rating})>"
