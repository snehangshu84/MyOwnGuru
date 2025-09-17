from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, get_current_user
from app.models.user import User
from app.schemas.learning_path import LearningPathWithSteps, LearningPathStepUpdate
from app.services.roadmap_generator import (
    generate_and_persist_learning_path,
    get_current_learning_path,
    update_step_progress,
    list_learning_paths,
    get_learning_path_by_id,
    restore_learning_path,
    compare_learning_paths,
)

router = APIRouter()

@router.post("/generate", response_model=LearningPathWithSteps)
def generate_roadmap(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    lp = generate_and_persist_learning_path(db, current_user)
    return lp

@router.get("/current", response_model=LearningPathWithSteps | None)
def current_roadmap(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    lp = get_current_learning_path(db, current_user)
    return lp

@router.patch("/steps/{step_id}", response_model=LearningPathWithSteps)
def update_step(
    step_id: int,
    payload: LearningPathStepUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    lp = update_step_progress(
        db,
        current_user,
        step_id,
        status=payload.status,
        progress_percentage=payload.progress_percentage,
    )
    return lp

@router.get("/history")
def history(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    rows = list_learning_paths(db, current_user)
    # Return lightweight metadata to keep payload small
    return [
        {
            "id": r.id,
            "title": r.title,
            "status": r.status,
            "created_at": r.created_at,
            "progress_percentage": r.progress_percentage,
            "estimated_duration_weeks": r.estimated_duration_weeks,
        }
        for r in rows
    ]

@router.get("/{path_id}")
def get_path(path_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    row = get_learning_path_by_id(db, current_user, path_id)
    return row

@router.post("/{path_id}/restore", response_model=LearningPathWithSteps)
def restore(path_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    lp = restore_learning_path(db, current_user, path_id)
    return lp

@router.post("/compare")
def compare(a_id: int, b_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    data = compare_learning_paths(db, current_user, a_id, b_id)
    return data
