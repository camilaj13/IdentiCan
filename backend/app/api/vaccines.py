from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.dog import Dog
from app.models.user import User
from app.models.vaccine import Vaccine
from app.schemas.vaccine import VaccineCreate, VaccineResponse

router = APIRouter(prefix="/api/vaccines", tags=["Vacunas"])


@router.post("", response_model=VaccineResponse, status_code=status.HTTP_201_CREATED)
def create_vaccine(
    data: VaccineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Registrar una vacuna para un perro."""
    dog = db.query(Dog).filter(Dog.id == data.dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tenés acceso a este perro")

    vaccine = Vaccine(**data.model_dump())
    db.add(vaccine)
    db.commit()
    db.refresh(vaccine)
    return VaccineResponse.model_validate(vaccine)


@router.get("/dog/{dog_id}", response_model=List[VaccineResponse])
def list_vaccines(
    dog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Listar todas las vacunas de un perro."""
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tenés acceso a este perro")

    vaccines = (
        db.query(Vaccine)
        .filter(Vaccine.dog_id == dog_id)
        .order_by(Vaccine.vaccine_date.desc())
        .all()
    )
    return [VaccineResponse.model_validate(v) for v in vaccines]


@router.delete("/{vaccine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vaccine(
    vaccine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Eliminar una vacuna."""
    vaccine = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")

    dog = db.query(Dog).filter(Dog.id == vaccine.dog_id).first()
    if not dog or (dog.owner_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="No tenés acceso a esta vacuna")

    db.delete(vaccine)
    db.commit()
