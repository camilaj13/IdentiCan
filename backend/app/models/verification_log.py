from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String

from app.core.database import Base


class VerificationLog(Base):
    __tablename__ = "verification_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=True)
    verification_type = Column(String(20), nullable=False)  # nose_scan, qr_scan
    success = Column(Boolean, nullable=False)
    confidence_score = Column(Float, nullable=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
