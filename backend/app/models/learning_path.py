"""
Learning path models for personalized learning roadmaps
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Path metadata
    title = Column(String, nullable=False)
    description = Column(Text)
    goal = Column(Text)  # What the user wants to achieve
    
    # Path characteristics
    difficulty_level = Column(String)  # beginner, intermediate, advanced
    estimated_duration_weeks = Column(Integer)
    category = Column(String)  # career_change, skill_upgrade, certification, etc.
    
    # Status and progress
    status = Column(String, default="active")  # active, paused, completed, archived
    progress_percentage = Column(Float, default=0.0)
    
    # AI generation metadata
    generated_by_ai = Column(Boolean, default=True)
    ai_confidence_score = Column(Float)
    generation_prompt = Column(Text)
    
    # Personalization factors
    user_preferences = Column(JSON)
    career_alignment_score = Column(Float)
    business_relevance_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    last_accessed = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="learning_paths")
    steps = relationship("LearningPathStep", back_populates="learning_path", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<LearningPath(id={self.id}, title='{self.title}', user_id={self.user_id})>"

class LearningPathStep(Base):
    __tablename__ = "learning_path_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    
    # Step details
    title = Column(String, nullable=False)
    description = Column(Text)
    step_number = Column(Integer, nullable=False)
    step_type = Column(String)  # course, tutorial, project, assessment, reading
    
    # Content and resources
    content_url = Column(String)
    content_provider = Column(String)  # coursera, udemy, youtube, github, etc.
    estimated_duration_hours = Column(Float)
    
    # Prerequisites and dependencies
    prerequisites = Column(JSON)  # List of required skills or previous steps
    dependencies = Column(JSON)  # Other steps that must be completed first
    
    # Status and progress
    status = Column(String, default="not_started")  # not_started, in_progress, completed, skipped
    progress_percentage = Column(Float, default=0.0)
    
    # Learning outcomes
    learning_objectives = Column(JSON)
    skills_gained = Column(JSON)
    difficulty_rating = Column(Float)
    
    # User interaction
    is_mandatory = Column(Boolean, default=True)
    user_rating = Column(Float)
    user_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    learning_path = relationship("LearningPath", back_populates="steps")
    
    def __repr__(self):
        return f"<LearningPathStep(id={self.id}, title='{self.title}', step_number={self.step_number})>"
