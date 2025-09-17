from __future__ import annotations
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.user import User
from app.models.skill import UserSkill
from app.models.learning_path import LearningPath, LearningPathStep
from app.schemas.learning_path import LearningPathWithSteps
from pathlib import Path
import json

_CURATED: Optional[Dict[str, List[Dict[str, Any]]]] = None

def _load_curated() -> Dict[str, List[Dict[str, Any]]]:
    global _CURATED
    if _CURATED is None:
        data_path = Path(__file__).resolve().parent.parent / "data" / "curated_content.json"
        if data_path.exists():
            _CURATED = json.loads(data_path.read_text(encoding="utf-8"))
        else:
            _CURATED = {}
    return _CURATED

def _pick_curated(skill_name: str, type_hint: str) -> Dict[str, Any]:
    curated = _load_curated()
    items = curated.get(skill_name, [])
    # Try to match by type first
    for it in items:
        if it.get("type", "").lower() == type_hint.lower():
            return it
    # Fallback to first available
    return items[0] if items else {}

def _draft_steps_from_skills(user_skills: List[UserSkill]) -> List[dict]:
    steps: List[dict] = []
    # Sort by priority and lowest proficiency
    ordered = sorted(
        user_skills,
        key=lambda us: (
            {"critical": 0, "high": 1, "medium": 2, "low": 3}.get((us.priority or "medium").lower(), 2),
            us.proficiency_level or 0.0,
        ),
    )
    step_no = 1
    for us in ordered:
        name = us.skill.name if us.skill else "Skill"
        # Compose a few step types per skill
        reading = _pick_curated(name, "reading")
        steps.append({
            "title": f"Primer: {name}",
            "description": f"Introductory concepts and foundations for {name}.",
            "step_number": step_no,
            "step_type": "reading",
            "estimated_duration_hours": 2.0,
            "content_provider": reading.get("provider", "curated"),
            "content_url": reading.get("url"),
            "learning_objectives": [f"Understand basics of {name}"],
            "skills_gained": [name],
        })
        step_no += 1
        course = _pick_curated(name, "course")
        steps.append({
            "title": f"Course: {name} fundamentals",
            "description": f"A guided course to solidify {name} fundamentals.",
            "step_number": step_no,
            "step_type": "course",
            "estimated_duration_hours": 6.0,
            "content_provider": course.get("provider", "web"),
            "content_url": course.get("url"),
            "learning_objectives": [f"Apply {name} in simple projects"],
            "skills_gained": [name],
        })
        step_no += 1
        steps.append({
            "title": f"Project: Build with {name}",
            "description": f"Hands-on mini project to practice {name}.",
            "step_number": step_no,
            "step_type": "project",
            "estimated_duration_hours": 8.0,
            "content_provider": "self-guided",
            "learning_objectives": [f"Create a small project using {name}"],
            "skills_gained": [name],
        })
        step_no += 1
        if step_no > 12:
            break
    return steps

def generate_and_persist_learning_path(db: Session, user: User) -> LearningPathWithSteps:
    # Load user's skills with joined Skill
    user_skills = (
        db.query(UserSkill)
        .options(joinedload(UserSkill.skill))
        .filter(UserSkill.user_id == user.id)
        .all()
    )

    # Deactivate existing active paths for user
    db.query(LearningPath).filter(LearningPath.user_id == user.id, LearningPath.status == "active").update({LearningPath.status: "archived"})

    # Create a new path
    lp = LearningPath(
        user_id=user.id,
        title=f"Roadmap for {user.full_name}",
        description="A tailored learning path based on your current skills and goals.",
        goal=user.career_goals or "Grow in current role",
        difficulty_level="intermediate",
        estimated_duration_weeks=6,
        category="skill_upgrade",
        status="active",
        progress_percentage=0.0,
        generated_by_ai=True,
    )
    db.add(lp)
    db.flush()

    # Draft steps from skills and persist
    steps_data = _draft_steps_from_skills(user_skills)
    for sd in steps_data:
        step = LearningPathStep(
            learning_path_id=lp.id,
            title=sd["title"],
            description=sd.get("description"),
            step_number=sd["step_number"],
            step_type=sd.get("step_type"),
            content_url=sd.get("content_url"),
            content_provider=sd.get("content_provider"),
            estimated_duration_hours=sd.get("estimated_duration_hours"),
            learning_objectives=sd.get("learning_objectives"),
            skills_gained=sd.get("skills_gained"),
            status="not_started",
        )
        db.add(step)
    db.commit()

    # Reload with steps
    full = (
        db.query(LearningPath)
        .options(joinedload(LearningPath.steps))
        .filter(LearningPath.id == lp.id)
        .first()
    )
    return full  # FastAPI + Pydantic from_attributes will serialize to LearningPathWithSteps

def get_current_learning_path(db: Session, user: User) -> LearningPathWithSteps | None:
    full = (
        db.query(LearningPath)
        .options(joinedload(LearningPath.steps))
        .filter(LearningPath.user_id == user.id, LearningPath.status == "active")
        .order_by(LearningPath.created_at.desc())
        .first()
    )
    return full

def list_learning_paths(db: Session, user: User) -> list[LearningPath]:
    rows = (
        db.query(LearningPath)
        .filter(LearningPath.user_id == user.id)
        .order_by(LearningPath.created_at.desc())
        .all()
    )
    return rows

def get_learning_path_by_id(db: Session, user: User, path_id: int) -> LearningPathWithSteps | None:
    row = (
        db.query(LearningPath)
        .options(joinedload(LearningPath.steps))
        .filter(LearningPath.user_id == user.id, LearningPath.id == path_id)
        .first()
    )
    return row

def restore_learning_path(db: Session, user: User, path_id: int) -> LearningPathWithSteps:
    target = get_learning_path_by_id(db, user, path_id)
    if not target:
        raise ValueError("LearningPath not found")
    # Archive current active
    db.query(LearningPath).filter(
        LearningPath.user_id == user.id, LearningPath.status == "active"
    ).update({LearningPath.status: "archived"})
    # Activate target
    target.status = "active"
    db.add(target)
    db.commit()
    refreshed = get_learning_path_by_id(db, user, target.id)
    return refreshed

def compare_learning_paths(db: Session, user: User, a_id: int, b_id: int) -> dict:
    a = get_learning_path_by_id(db, user, a_id)
    b = get_learning_path_by_id(db, user, b_id)
    if not a or not b:
        raise ValueError("One or both learning paths not found")
    a_steps = {(s.title or "").strip().lower() for s in a.steps}
    b_steps = {(s.title or "").strip().lower() for s in b.steps}
    intersection = sorted(list(a_steps & b_steps))
    only_a = sorted(list(a_steps - b_steps))
    only_b = sorted(list(b_steps - a_steps))
    return {
        "a": {"id": a.id, "title": a.title, "created_at": str(a.created_at), "steps_count": len(a.steps)},
        "b": {"id": b.id, "title": b.title, "created_at": str(b.created_at), "steps_count": len(b.steps)},
        "overlap_titles": intersection,
        "only_a_titles": only_a,
        "only_b_titles": only_b,
    }

def _recalculate_path_progress(db: Session, lp: LearningPath) -> None:
    if not lp.steps:
        lp.progress_percentage = 0.0
        return
    # Average of step progress; completed counts as 100 if not set
    total = 0.0
    count = 0
    for st in lp.steps:
        prog = st.progress_percentage if st.progress_percentage is not None else (100.0 if (st.status or "") == "completed" else 0.0)
        total += float(prog)
        count += 1
    lp.progress_percentage = round(total / max(count, 1), 2)

def update_step_progress(
    db: Session,
    user: User,
    step_id: int,
    *,
    status: str | None = None,
    progress_percentage: float | None = None,
) -> LearningPathWithSteps:
    # Load step with its path and ensure ownership
    step = (
        db.query(LearningPathStep)
        .join(LearningPath, LearningPath.id == LearningPathStep.learning_path_id)
        .options(joinedload(LearningPathStep.learning_path).joinedload(LearningPath.steps))
        .filter(LearningPathStep.id == step_id, LearningPath.user_id == user.id)
        .first()
    )
    if not step:
        raise ValueError("Step not found or not owned by user")

    if status is not None:
        step.status = status
    if progress_percentage is not None:
        # clamp 0..100
        step.progress_percentage = float(max(0.0, min(100.0, progress_percentage)))

    db.add(step)
    db.flush()

    # Recalculate path progress
    lp = step.learning_path
    _recalculate_path_progress(db, lp)
    db.add(lp)
    db.commit()

    # Return the full path with steps
    full = (
        db.query(LearningPath)
        .options(joinedload(LearningPath.steps))
        .filter(LearningPath.id == lp.id)
        .first()
    )
    return full
