from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.i18n import get_language, t
from app.models.dog import Dog
from app.models.user import User
from app.schemas.dog import DogCreate, DogResponse, DogUpdate

router = APIRouter(prefix="/api/dogs", tags=["Perros"])


def _generate_qr_code(dog_id: int) -> str:
    """Generate a unique QR code identifier for a dog."""
    return f"IDC-DOG-{dog_id:05d}"


@router.post("", response_model=DogResponse, status_code=status.HTTP_201_CREATED)
def create_dog(
    data: DogCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Registrar un nuevo perro."""
    dog = Dog(
        owner_id=current_user.id,
        qr_code="TEMP",  # Placeholder, updated after commit
        **data.model_dump(),
    )
    db.add(dog)
    db.commit()
    db.refresh(dog)

    # Set final QR code with the real ID
    dog.qr_code = _generate_qr_code(dog.id)
    db.commit()
    db.refresh(dog)

    return DogResponse.model_validate(dog)


@router.get("", response_model=List[DogResponse])
def list_dogs(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Listar los perros del usuario autenticado."""
    dogs = db.query(Dog).filter(Dog.owner_id == current_user.id).all()
    return [DogResponse.model_validate(d) for d in dogs]


@router.get("/{dog_id}", response_model=DogResponse)
def get_dog(
    dog_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtener un perro por ID."""
    lang = get_language(request)
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail=t("dog_not_found", lang))
    # Allow owner or admin to view
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("dog_no_access", lang))
    return DogResponse.model_validate(dog)


@router.put("/{dog_id}", response_model=DogResponse)
def update_dog(
    dog_id: int,
    data: DogUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualizar datos de un perro (solo el dueño)."""
    lang = get_language(request)
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail=t("dog_not_found", lang))
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("dog_only_owner_edit", lang))

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dog, field, value)

    db.commit()
    db.refresh(dog)
    return DogResponse.model_validate(dog)


@router.delete("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dog(
    dog_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Eliminar un perro (solo el dueño)."""
    lang = get_language(request)
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail=t("dog_not_found", lang))
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("dog_only_owner_delete", lang))

    db.delete(dog)
    db.commit()
