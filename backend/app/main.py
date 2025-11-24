from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine
from .deps import get_db
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="APIN Backend – AI Parking Spot Intelligence Network (MVP)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/lots", response_model=schemas.Lot)
def create_lot(lot_in: schemas.LotCreate, db: Session = Depends(get_db)):
    return crud.create_lot(db, lot_in)


@app.get("/lots", response_model=list[schemas.Lot])
def list_lots(db: Session = Depends(get_db)):
    return crud.get_lots(db)


@app.get("/lots/{lot_id}", response_model=schemas.Lot)
def get_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = crud.get_lot(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return lot


@app.post("/lots/{lot_id}/cameras", response_model=schemas.Camera)
def create_camera(lot_id: int, camera_in: schemas.CameraCreate, db: Session = Depends(get_db)):
    lot = crud.get_lot(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return crud.create_camera(db, lot_id, camera_in)


@app.get("/lots/{lot_id}/cameras", response_model=list[schemas.Camera])
def get_cameras_for_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = crud.get_lot(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return crud.get_cameras_for_lot(db, lot_id)


@app.post("/lots/{lot_id}/spots", response_model=list[schemas.Spot])
def create_spots(lot_id: int, spots_in: list[schemas.SpotCreate], db: Session = Depends(get_db)):
    lot = crud.get_lot(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return crud.create_spots(db, lot_id, spots_in)


@app.get("/lots/{lot_id}/spots", response_model=list[schemas.Spot])
def get_spots_for_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = crud.get_lot(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return crud.get_spots_for_lot(db, lot_id)


@app.put("/spots/{spot_id}/status", response_model=schemas.Spot)
def update_spot_status(spot_id: int, status_in: schemas.SpotStatusUpdate, db: Session = Depends(get_db)):
    spot = crud.update_spot_status(db, spot_id, status_in)
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    return spot


@app.get("/availability", response_model=list[schemas.LotAvailability])
def availability(db: Session = Depends(get_db)):
    return crud.get_availability(db)
