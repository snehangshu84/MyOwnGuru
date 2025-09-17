"""
Configuration settings for MyOwnGuru application
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MyOwnGuru"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Database Configuration
    DATABASE_URL: str = "postgresql+psycopg://username:password@localhost:5432/myownguru"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    
    # External API Keys
    COURSERA_API_KEY: Optional[str] = None
    UDEMY_API_KEY: Optional[str] = None
    YOUTUBE_API_KEY: Optional[str] = None
    
    # Email Configuration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIRECTORY: str = "uploads"
    ALLOWED_EXTENSIONS: set = {".pdf", ".doc", ".docx", ".txt"}
    
    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str]) -> str:
        if isinstance(v, str):
            return v
        return "postgresql+psycopg://username:password@localhost:5432/myownguru"

settings = Settings()
