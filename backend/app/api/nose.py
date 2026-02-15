import random
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.dog import Dog
from app.models.user import User
from app.models.verification_log import VerificationLog
from app.utils.storage import upload_image

router = APIRouter(prefix="/api/nose", tags=["Nariz / Biometría"])


def _check_verification_limit(user: User, db: Session) -> dict:
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
                "error": "Límite diario alcanzado",
                "verifications_used": count,
                "verifications_limit": limit,
                "message": "Upgrade a Premium para verificaciones ilimitadas",
            },
        )
    return {"limit": limit, "used": count, "remaining": limit - count}


@router.post("/upload")
def upload_nose_images(
    dog_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload nose images for a dog (up to 3 images).
    These images will be used for biometric identification.
    """
    dog = db.query(Dog).filter(Dog.id == dog_id, Dog.owner_id == current_user.id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Perro no encontrado")

    if len(files) > 3:
        raise HTTPException(status_code=400, detail="Máximo 3 imágenes permitidas")

    urls = []
    for f in files:
        if not f.content_type or not f.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"Archivo {f.filename} no es una imagen")
        content = f.file.read()
        url = upload_image(content, f.filename or "nose.jpg", folder="noses")
        urls.append(url)

    dog.nose_images = urls
    # In a real implementation, we would also compute nose_embedding here
    dog.nose_embedding = None
    db.commit()
    db.refresh(dog)

    return {
        "message": "Imágenes de nariz subidas correctamente",
        "dog_id": dog.id,
        "nose_images": dog.nose_images,
    }


@router.post("/verify")
def verify_nose(
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
    usage = _check_verification_limit(current_user, db)

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

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
            "Se encontró una coincidencia" if mock_match else "No se encontró coincidencia"
        ),
    }
