from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class SpotStatus(str, Enum):
    free = "free"
    occupied = "occupied"
    unknown = "unknown"


class CameraBase(BaseModel):
    name: str
    stream_url: Optional[str] = None
    zone: Optional[str] = None


class CameraCreate(CameraBase):
    pass


class Camera(CameraBase):
    id: int
    lot_id: int

    class Config:
        orm_mode = True


class SpotBase(BaseModel):
    label: str


class SpotCreate(SpotBase):
    camera_id: Optional[int] = None


class Spot(SpotBase):
    id: int
    lot_id: int
    camera_id: Optional[int] = None
    status: SpotStatus
    last_updated: datetime

    class Config:
        orm_mode = True


class SpotStatusUpdate(BaseModel):
    status: SpotStatus


class LotBase(BaseModel):
    name: str
    location: Optional[str] = None
    campus: Optional[str] = None


class LotCreate(LotBase):
    pass


class Lot(LotBase):
    id: int
    cameras: List[Camera] = []
    spots: List[Spot] = []

    class Config:
        orm_mode = True


class LotAvailability(BaseModel):
    lot_id: int
    lot_name: str
    total_spots: int
    free_spots: int
    occupied_spots: int
    unknown_spots: int
