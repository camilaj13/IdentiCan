import logging
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
from app.utils.ml_engine import (
    compute_similarity,
    extract_embedding,
    extract_embedding_multi,
    find_best_match,
)
from app.utils.storage import upload_image

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/nose", tags=["Nose / Biometrics"])

# Cosine-similarity threshold for a positive match (from config).
MATCH_THRESHOLD = settings.MATCH_THRESHOLD


def _check_verification_limit(user: User, db: Session, lang: str = "es") -> dict:
    """
    Check if the user has reached the daily verification limit.
    Only admin users have unlimited verifications.
    Returns usage info dict. Raises HTTPException if limit reached.
    """
    if user.role == "admin":
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

    Stores the images and computes a biometric embedding using the
    Pet-ReID-IMAG model (ResNeSt-101 backbone, 2048-dim embedding).
    The averaged embedding is persisted in the dog record for later
    verification matching.
    """
    lang = get_language(request)
    dog = db.query(Dog).filter(Dog.id == dog_id, Dog.owner_id == current_user.id).first()
    if not dog:
        raise HTTPException(status_code=404, detail=t("dog_not_found", lang))

    if len(files) > 3:
        raise HTTPException(status_code=400, detail=t("max_images", lang))

    urls = []
    images_bytes: List[bytes] = []

    for f in files:
        if not f.content_type or not f.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=t("file_not_image", lang, filename=f.filename))
        content = f.file.read()
        url = upload_image(content, f.filename or "nose.jpg", folder="noses")
        urls.append(url)
        images_bytes.append(content)

    dog.nose_images = urls

    # Compute the nose embedding using Pet-ReID-IMAG model
    try:
        if len(images_bytes) == 1:
            embedding = extract_embedding(images_bytes[0])
        else:
            embedding = extract_embedding_multi(images_bytes)
        dog.nose_embedding = embedding
        logger.info("Computed nose embedding for dog %d (%d images, dim=%d)", dog.id, len(images_bytes), len(embedding))
    except Exception:
        logger.exception("Failed to compute nose embedding for dog %d", dog.id)
        raise HTTPException(
            status_code=500,
            detail="Failed to compute nose embedding. Please try again with a clear photo of the dog's nose.",
        )

    db.commit()
    db.refresh(dog)

    return {
        "message": t("nose_images_uploaded", lang),
        "dog_id": dog.id,
        "nose_images": dog.nose_images,
        "embedding_computed": dog.nose_embedding is not None,
        "embedding_dim": len(dog.nose_embedding) if dog.nose_embedding else 0,
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

    Extracts an embedding from the uploaded nose photo using the
    Pet-ReID-IMAG model, then compares it against all stored dog
    embeddings using cosine similarity. Returns the best match
    above the confidence threshold.

    Limits: 3 verifications per day for all regular users (free and premium).
    Only admin users have unlimited verifications.
    """
    lang = get_language(request)
    usage = _check_verification_limit(current_user, db, lang)

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail=t("must_be_image", lang))

    image_bytes = file.file.read()

    # Extract embedding from the uploaded nose photo
    try:
        query_embedding = extract_embedding(image_bytes)
    except Exception:
        logger.exception("Failed to extract embedding from verification image")
        raise HTTPException(
            status_code=500,
            detail="Failed to process the nose image. Please try again with a clear photo.",
        )

    # Load all dogs that have a stored nose embedding
    dogs_with_embeddings = (
        db.query(Dog)
        .filter(Dog.nose_embedding.isnot(None))
        .all()
    )

    gallery = [
        (dog.id, dog.nose_embedding)
        for dog in dogs_with_embeddings
        if dog.nose_embedding
    ]

    # Find best match
    result = find_best_match(query_embedding, gallery, threshold=MATCH_THRESHOLD)

    if result:
        matched_dog_id, confidence = result
        matched_dog = db.query(Dog).filter(Dog.id == matched_dog_id).first()
        is_match = True
    else:
        matched_dog_id = None
        matched_dog = None
        confidence = 0.0
        # If gallery is non-empty, report the best score even if below threshold
        if gallery:
            best_sim = max(
                compute_similarity(query_embedding, emb) for _, emb in gallery
            )
            confidence = best_sim
        is_match = False

    # Log the verification
    log = VerificationLog(
        user_id=current_user.id,
        dog_id=matched_dog_id,
        verification_type="nose_scan",
        success=is_match,
        confidence_score=round(confidence, 4),
        date=date.today(),
    )
    db.add(log)
    db.commit()

    return {
        "match": is_match,
        "confidence": round(confidence, 4),
        "dog_id": matched_dog_id,
        "dog_name": matched_dog.name if matched_dog else None,
        "verification_usage": usage,
        "message": (
            t("match_found", lang) if is_match else t("no_match_found", lang)
        ),
    }
