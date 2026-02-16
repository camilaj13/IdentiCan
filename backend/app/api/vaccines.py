from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.i18n import get_language, t
from app.models.dog import Dog
from app.models.user import User
from app.models.vaccine import Vaccine
from app.schemas.vaccine import VaccineCreate, VaccineResponse

router = APIRouter(prefix="/api/vaccines", tags=["Vaccines"])


@router.post("", response_model=VaccineResponse, status_code=status.HTTP_201_CREATED)
def create_vaccine(
    data: VaccineCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Register a vaccine for a dog."""
    lang = get_language(request)
    dog = db.query(Dog).filter(Dog.id == data.dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail=t("dog_not_found", lang))
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("dog_no_access", lang))

    vaccine = Vaccine(**data.model_dump())
    db.add(vaccine)
    db.commit()
    db.refresh(vaccine)
    return VaccineResponse.model_validate(vaccine)


@router.get("/dog/{dog_id}", response_model=List[VaccineResponse])
def list_vaccines(
    dog_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all vaccines for a dog."""
    lang = get_language(request)
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail=t("dog_not_found", lang))
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("dog_no_access", lang))

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
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a vaccine."""
    lang = get_language(request)
    vaccine = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail=t("vaccine_not_found", lang))

    dog = db.query(Dog).filter(Dog.id == vaccine.dog_id).first()
    if not dog or (dog.owner_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail=t("vaccine_no_access", lang))

    db.delete(vaccine)
    db.commit()
