from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import item as models
from schemas import item_schema as schemas
from auth.security import get_current_user

router = APIRouter(prefix="/items", tags=["Alat Camping"])

# Create Item - Status 201
@router.post("/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Read All Items
@router.get("/", response_model=List[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

# Read Item by ID
@router.get("/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Alat camping tidak ditemukan")
    return item

# Update Item
@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item_data: schemas.ItemCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Alat tidak ditemukan")
    
    for key, value in item_data.model_dump().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

# Delete Item - Terproteksi JWT
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Alat tidak ditemukan")
    
    db.delete(db_item)
    db.commit()
    return None