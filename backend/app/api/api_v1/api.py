"""
API v1 router aggregator
"""
from fastapi import APIRouter
from .endpoints import auth, users, resume, roadmap, recommendations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(roadmap.router, prefix="/roadmap", tags=["roadmap"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
