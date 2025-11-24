from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class SpotStatus(str, Enum):
    FREE = "free"
    OCCUPIED = "occupied"
    UNKNOWN = "unknown"


class Lot(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    campus = Column(String, nullable=True)

    cameras = relationship("Camera", back_populates="lot", cascade="all, delete-orphan")
    spots = relationship("Spot", back_populates="lot", cascade="all, delete-orphan")


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(Integer, ForeignKey("lots.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    stream_url = Column(String, nullable=True)
    zone = Column(String, nullable=True)

    lot = relationship("Lot", back_populates="cameras")
    spots = relationship("Spot", back_populates="camera")


class Spot(Base):
    __tablename__ = "spots"

    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(Integer, ForeignKey("lots.id", ondelete="CASCADE"), nullable=False)
    camera_id = Column(Integer, ForeignKey("cameras.id", ondelete="SET NULL"), nullable=True)

    label = Column(String, nullable=False)
    status = Column(SqlEnum(SpotStatus), default=SpotStatus.UNKNOWN, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

    lot = relationship("Lot", back_populates="spots")
    camera = relationship("Camera", back_populates="spots")
