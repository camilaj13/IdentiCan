from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False, index=True)
    vaccine_type = Column(String(100), nullable=False)
    vaccine_date = Column(Date, nullable=False)
    next_dose_date = Column(Date, nullable=True)
    veterinarian_name = Column(String(200), nullable=True)
    clinic_name = Column(String(200), nullable=True)
    batch_number = Column(String(100), nullable=True)
    certificate_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    dog = relationship("Dog", back_populates="vaccines")
