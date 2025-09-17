"""
Skill models for tracking user skills and competencies
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)  # technical, soft, domain-specific
    subcategory = Column(String)
    description = Column(Text)
    
    # Skill metadata
    is_trending = Column(Boolean, default=False)
    difficulty_level = Column(String)  # beginner, intermediate, advanced, expert
    market_demand = Column(Float, default=0.0)  # 0-100 scale
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill")
    
    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}', category='{self.category}')>"

class UserSkill(Base):
    __tablename__ = "user_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    
    # Skill proficiency and assessment
    proficiency_level = Column(Float, nullable=False)  # 0-100 scale
    confidence_level = Column(Float)  # 0-100 scale (self-assessed)
    years_of_experience = Column(Float)
    
    # Source of skill assessment
    source = Column(String)  # resume, linkedin, github, self-assessment, test
    evidence = Column(Text)  # Projects, certifications, etc.
    
    # Learning status
    is_learning_goal = Column(Boolean, default=False)
    target_proficiency = Column(Float)
    priority = Column(String, default="medium")  # low, medium, high, critical
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_assessed = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")
    
    def __repr__(self):
        return f"<UserSkill(user_id={self.user_id}, skill_id={self.skill_id}, proficiency={self.proficiency_level})>"
