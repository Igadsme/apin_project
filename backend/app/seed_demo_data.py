# Seed demo data for APIN

from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, crud, schemas


def seed() -> None:
    models.Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        if crud.get_lots(db):
            print("Lots already exist, skipping seed.")
            return

        lot = crud.create_lot(
            db,
            schemas.LotCreate(
                name="Campus Garage A",
                location="North Campus",
                campus="Main Campus",
            ),
        )

        cam1 = crud.create_camera(
            db,
            lot.id,
            schemas.CameraCreate(
                name="Entrance Cam",
                stream_url="rtsp://demo/entrance",
                zone="Level 1",
            ),
        )
        cam2 = crud.create_camera(
            db,
            lot.id,
            schemas.CameraCreate(
                name="Roof Cam",
                stream_url="rtsp://demo/roof",
                zone="Level 5",
            ),
        )

        spots_in = []
        for i in range(1, 11):
            spots_in.append(
                schemas.SpotCreate(
                    label=f"L1-{i:02d}",
                    camera_id=cam1.id,
                )
            )
        for i in range(1, 11):
            spots_in.append(
                schemas.SpotCreate(
                    label=f"L5-{i:02d}",
                    camera_id=cam2.id,
                )
            )

        crud.create_spots(db, lot.id, spots_in)
        print("Seeded demo lot, cameras, and spots.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
