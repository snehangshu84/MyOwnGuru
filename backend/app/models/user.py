"""
User model for authentication and profile management
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Profile information
    job_title = Column(String)
    company = Column(String)
    industry = Column(String)
    experience_level = Column(String)  # junior, mid, senior, expert
    career_goals = Column(Text)
    preferred_learning_style = Column(String)  # visual, auditory, kinesthetic, reading
    
    # Resume and profile data
    resume_text = Column(Text)
    resume_filename = Column(String)
    linkedin_profile = Column(String)
    github_profile = Column(String)
    portfolio_url = Column(String)
    
    # Preferences
    learning_preferences = Column(JSON)  # Store as JSON for flexibility
    notification_preferences = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPath", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
