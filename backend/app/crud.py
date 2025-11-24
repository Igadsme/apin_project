from sqlalchemy.orm import Session
from sqlalchemy import func, case

from . import models, schemas


def create_lot(db: Session, lot_in: schemas.LotCreate) -> models.Lot:
    lot = models.Lot(
        name=lot_in.name,
        location=lot_in.location,
        campus=lot_in.campus,
    )
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot


def get_lots(db: Session):
    return db.query(models.Lot).all()


def get_lot(db: Session, lot_id: int):
    return db.query(models.Lot).filter(models.Lot.id == lot_id).first()


def create_camera(db: Session, lot_id: int, camera_in: schemas.CameraCreate) -> models.Camera:
    camera = models.Camera(
        lot_id=lot_id,
        name=camera_in.name,
        stream_url=camera_in.stream_url,
        zone=camera_in.zone,
    )
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera


def get_cameras_for_lot(db: Session, lot_id: int):
    return db.query(models.Camera).filter(models.Camera.lot_id == lot_id).all()


def create_spots(db: Session, lot_id: int, spots_in: list[schemas.SpotCreate]) -> list[models.Spot]:
    spots: list[models.Spot] = []
    for spot_in in spots_in:
        spot = models.Spot(
            lot_id=lot_id,
            camera_id=spot_in.camera_id,
            label=spot_in.label,
        )
        db.add(spot)
        spots.append(spot)
    db.commit()
    for spot in spots:
        db.refresh(spot)
    return spots


def get_spots_for_lot(db: Session, lot_id: int):
    return db.query(models.Spot).filter(models.Spot.lot_id == lot_id).all()


def update_spot_status(db: Session, spot_id: int, status_in: schemas.SpotStatusUpdate):
    spot = db.query(models.Spot).filter(models.Spot.id == spot_id).first()
    if not spot:
        return None
    from datetime import datetime

    spot.status = models.SpotStatus(status_in.status.value)
    spot.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(spot)
    return spot


def get_availability(db: Session) -> list[schemas.LotAvailability]:
    rows = (
        db.query(
            models.Lot.id.label("lot_id"),
            models.Lot.name.label("lot_name"),
            func.count(models.Spot.id).label("total_spots"),
            func.sum(case((models.Spot.status == models.SpotStatus.FREE, 1), else_=0)).label("free_spots"),
            func.sum(case((models.Spot.status == models.SpotStatus.OCCUPIED, 1), else_=0)).label("occupied_spots"),
            func.sum(case((models.Spot.status == models.SpotStatus.UNKNOWN, 1), else_=0)).label("unknown_spots"),
        )
        .outerjoin(models.Spot, models.Spot.lot_id == models.Lot.id)
        .group_by(models.Lot.id)
        .all()
    )

    return [
        schemas.LotAvailability(
            lot_id=row.lot_id,
            lot_name=row.lot_name,
            total_spots=row.total_spots or 0,
            free_spots=row.free_spots or 0,
            occupied_spots=row.occupied_spots or 0,
            unknown_spots=row.unknown_spots or 0,
        )
        for row in rows
    ]
