from __future__ import annotations
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.schemas.skill import UserSkillOut
from app.models.skill import Skill, UserSkill
from app.models.user import User
from app.services.skills_service import extract_skills_from_text

from pathlib import Path

def _read_text_from_pdf(data: bytes) -> str:
    try:
        from PyPDF2 import PdfReader
        import io
        reader = PdfReader(io.BytesIO(data))
        parts: List[str] = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        return "\n".join(parts)
    except Exception:
        return ""

def _read_text_from_docx(data: bytes) -> str:
    try:
        import io
        from docx import Document
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception:
        return ""

def _read_text_from_plain(data: bytes) -> str:
    for enc in ("utf-8", "latin-1", "utf-16"):
        try:
            return data.decode(enc)
        except Exception:
            continue
    return ""

async def persist_user_skills_from_resume(
    file: UploadFile, db: Session, user: User
) -> List[UserSkillOut]:
    # Read file bytes
    content = await file.read()
    suffix = Path(file.filename or "").suffix.lower()

    # Extract text based on type
    text = ""
    if suffix == ".pdf":
        text = _read_text_from_pdf(content)
    elif suffix in (".docx",):
        text = _read_text_from_docx(content)
    else:
        text = _read_text_from_plain(content)

    # Fallback if no text
    if not text:
        text = _read_text_from_plain(content)

    # Extract skills using taxonomy matching
    triples = extract_skills_from_text(text)

    user_skill_out: List[UserSkillOut] = []

    for name, category, subcategory in triples:
        # Find or create Skill
        skill = db.query(Skill).filter(Skill.name == name).first()
        if not skill:
            skill = Skill(
                name=name,
                category="technical",  # using taxonomy category
                subcategory=subcategory,
                description=None,
            )
            db.add(skill)
            db.flush()  # get skill.id without full commit

        # Check existing UserSkill
        us = (
            db.query(UserSkill)
            .filter(UserSkill.user_id == user.id, UserSkill.skill_id == skill.id)
            .first()
        )
        if not us:
            us = UserSkill(
                user_id=user.id,
                skill_id=skill.id,
                proficiency_level=30.0,  # initial estimate
                confidence_level=50.0,
                years_of_experience=None,
                source="resume",
                evidence=f"Detected in resume: {name}",
                is_learning_goal=False,
                target_proficiency=70.0,
                priority="medium",
            )
            db.add(us)
            db.flush()

        user_skill_out.append(
            UserSkillOut(
                id=us.id,
                skill_id=skill.id,
                proficiency_level=us.proficiency_level,
                confidence_level=us.confidence_level,
                years_of_experience=us.years_of_experience,
                source=us.source,
                evidence=us.evidence,
                is_learning_goal=us.is_learning_goal,
                target_proficiency=us.target_proficiency,
                priority=us.priority,
            )
        )

    db.commit()
    return user_skill_out
