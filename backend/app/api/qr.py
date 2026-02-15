from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.dog import Dog
from app.models.user import User
from app.utils.qr_generator import generate_qr_pdf, generate_qr_png

router = APIRouter(prefix="/api/qr", tags=["Código QR"])


@router.get("/generate/{dog_id}")
def generate_qr(
    dog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generar código QR en formato PNG para un perro."""
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tenés acceso a este perro")

    png_bytes = generate_qr_png(dog.qr_code)
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={"Content-Disposition": f'inline; filename="qr_{dog.qr_code}.png"'},
    )


@router.get("/pdf/{dog_id}")
def generate_qr_pdf_endpoint(
    dog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generar código QR en formato PDF 3x3cm para un perro."""
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Perro no encontrado")
    if dog.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tenés acceso a este perro")

    pdf_bytes = generate_qr_pdf(dog.qr_code, dog_name=dog.name)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="qr_{dog.qr_code}.pdf"'},
    )
