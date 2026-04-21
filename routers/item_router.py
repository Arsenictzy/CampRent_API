from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import item as models
from schemas import item_schema as schemas
from auth.security import get_current_user

# Kita gunakan prefix root "/" agar lebih fleksibel dalam satu file
router = APIRouter(tags=["Manajemen CampRent"])

# --- ENDPOINT CATEGORY (Entitas 1) ---

@router.post("/categories", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Mengecek apakah kategori sudah ada
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Kategori sudah ada")
    
    new_cat = models.Category(name=category.name)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


# --- ENDPOINT ITEMS (Entitas 2 - Berelasi dengan Category) ---

# Create Item - Wajib Token
@router.post("/items", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Validasi: Apakah category_id yang diinput ada di database?
    category = db.query(models.Category).filter(models.Category.id == item.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category ID tidak ditemukan. Buat kategori dulu!")

    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Read All Items - Publik
@router.get("/items", response_model=List[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

# Read Item by ID - Publik
@router.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Alat camping tidak ditemukan")
    return item

# Update Item - Wajib Token
@router.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item_data: schemas.ItemCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Alat tidak ditemukan")
    
    for key, value in item_data.model_dump().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

# Delete Item - Wajib Token
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Alat tidak ditemukan")
    
    db.delete(db_item)
    db.commit()
    return None