import random
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.i18n import get_language, t
from app.models.dog import Dog
from app.models.user import User
from app.models.verification_log import VerificationLog
from app.utils.storage import upload_image

router = APIRouter(prefix="/api/nose", tags=["Nose / Biometrics"])


def _check_verification_limit(user: User, db: Session, lang: str = "es") -> dict:
    """
    Check if the user has reached the daily verification limit.
    Returns usage info dict. Raises HTTPException if limit reached.
    """
    if user.role == "admin" or user.is_premium:
        return {"limit": None, "used": 0, "remaining": None}

    today = date.today()
    count = (
        db.query(VerificationLog)
        .filter(
            VerificationLog.user_id == user.id,
            VerificationLog.date == today,
        )
        .count()
    )
    limit = settings.VERIFICATION_LIMIT_FREE

    if count >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": t("daily_limit_reached", lang),
                "verifications_used": count,
                "verifications_limit": limit,
                "message": t("upgrade_premium", lang),
            },
        )
    return {"limit": limit, "used": count, "remaining": limit - count}


@router.post("/upload")
def upload_nose_images(
    dog_id: int,
    request: Request,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload nose images for a dog (up to 3 images).
    These images will be used for biometric identification.
    """
    lang = get_language(request)
    dog = db.query(Dog).filter(Dog.id == dog_id, Dog.owner_id == current_user.id).first()
    if not dog:
        raise HTTPException(status_code=404, detail=t("dog_not_found", lang))

    if len(files) > 3:
        raise HTTPException(status_code=400, detail=t("max_images", lang))

    urls = []
    for f in files:
        if not f.content_type or not f.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=t("file_not_image", lang, filename=f.filename))
        content = f.file.read()
        url = upload_image(content, f.filename or "nose.jpg", folder="noses")
        urls.append(url)

    dog.nose_images = urls
    # In a real implementation, we would also compute nose_embedding here
    dog.nose_embedding = None
    db.commit()
    db.refresh(dog)

    return {
        "message": t("nose_images_uploaded", lang),
        "dog_id": dog.id,
        "nose_images": dog.nose_images,
    }


@router.post("/verify")
def verify_nose(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Verify a dog's identity by nose scan.

    Limits: 3 verifications per day for free users.
    Premium and admin users have unlimited verifications.

    Currently returns a mock result. Real ML matching will be
    integrated when the nose-print model is ready.
    """
    lang = get_language(request)
    usage = _check_verification_limit(current_user, db, lang)

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail=t("must_be_image", lang))

    # --- MOCK VERIFICATION ---
    # In production, this would:
    # 1. Extract nose embedding from uploaded image
    # 2. Compare against all stored embeddings
    # 3. Return the closest match above a confidence threshold
    mock_confidence = round(random.uniform(0.65, 0.98), 4)
    mock_match = mock_confidence > 0.85

    # Find a random dog to pretend it matched (for demo purposes)
    matched_dog = db.query(Dog).first()
    matched_dog_id = matched_dog.id if matched_dog and mock_match else None

    # Log the verification
    log = VerificationLog(
        user_id=current_user.id,
        dog_id=matched_dog_id,
        verification_type="nose_scan",
        success=mock_match,
        confidence_score=mock_confidence,
        date=date.today(),
    )
    db.add(log)
    db.commit()

    return {
        "match": mock_match,
        "confidence": mock_confidence,
        "dog_id": matched_dog_id,
        "dog_name": matched_dog.name if matched_dog and mock_match else None,
        "verification_usage": usage,
        "message": (
            t("match_found", lang) if mock_match else t("no_match_found", lang)
        ),
    }
