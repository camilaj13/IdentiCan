from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=True)
    age_years = Column(Integer, nullable=True)
    weight_kg = Column(Float, nullable=True)
    sex = Column(String(1), nullable=False)  # M / F
    color = Column(String(100), nullable=True)
    origin = Column(String(50), nullable=False)  # adopted/purchased/rescued/other
    nose_images = Column(JSON, default=list)  # ["url1", "url2", "url3"]
    nose_embedding = Column(JSON, nullable=True)  # [512 floats]
    qr_code = Column(String(20), unique=True, index=True)
    microchip_id = Column(String(50), nullable=True)
    behavior_notes = Column(Text, nullable=True)
    likes = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    from_shelter = Column(Boolean, default=False)
    shelter_name = Column(String(200), nullable=True)
    previous_owner_name = Column(String(200), nullable=True)
    health_booklet_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    owner = relationship("User", backref="dogs")
    vaccines = relationship("Vaccine", back_populates="dog", cascade="all, delete-orphan")
