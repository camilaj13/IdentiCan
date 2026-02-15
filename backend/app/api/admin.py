from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.dog import Dog
from app.models.user import User
from app.models.verification_log import VerificationLog
from app.schemas.dog import DogResponse
from app.schemas.user import UserResponse

router = APIRouter(prefix="/api/admin", tags=["Administración"])

admin_only = require_role("admin")


@router.get("/users", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    """Listar todos los usuarios (solo admin)."""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [UserResponse.model_validate(u) for u in users]


@router.get("/dogs", response_model=List[DogResponse])
def list_all_dogs(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    """Listar todos los perros registrados (solo admin)."""
    dogs = db.query(Dog).order_by(Dog.created_at.desc()).all()
    return [DogResponse.model_validate(d) for d in dogs]


@router.post("/users/{user_id}/premium")
def toggle_premium(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    """Activar/desactivar Premium para un usuario (solo admin)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.is_premium = not user.is_premium
    db.commit()
    db.refresh(user)

    return {
        "message": f"Premium {'activado' if user.is_premium else 'desactivado'} para {user.name}",
        "user_id": user.id,
        "is_premium": user.is_premium,
    }


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    """Obtener estadísticas generales (solo admin)."""
    total_users = db.query(User).count()
    premium_users = db.query(User).filter(User.is_premium.is_(True)).count()
    total_dogs = db.query(Dog).count()
    total_verifications = db.query(VerificationLog).count()
    successful_verifications = (
        db.query(VerificationLog).filter(VerificationLog.success.is_(True)).count()
    )

    return {
        "total_users": total_users,
        "premium_users": premium_users,
        "total_dogs": total_dogs,
        "total_verifications": total_verifications,
        "successful_verifications": successful_verifications,
        "success_rate": (
            round(successful_verifications / total_verifications * 100, 1)
            if total_verifications > 0
            else 0
        ),
    }
