from pydantic import BaseModel, Field
from typing import List, Optional

# --- Schema untuk User (Wajib untuk Register & Login) ---
class UserCreate(BaseModel):
    # Parameter example dihapus agar input kosong di Swagger
    username: str = Field(..., min_length=3) 
    password: str = Field(..., min_length=6)

# --- Schema untuk Item (Alat Camping) ---
class ItemBase(BaseModel):
    # Menghapus example agar mahasiswa/user harus mengisi sendiri
    name: str = Field(..., min_length=3)
    stock: int = Field(..., gt=0) # Validasi: stok harus lebih dari 0

class ItemCreate(ItemBase):
    category_id: int

class ItemResponse(ItemBase):
    id: int
    category_id: int
    
    class Config:
        # Menggunakan from_attributes agar kompatibel dengan SQLAlchemy 
        from_attributes = True 

# --- Schema untuk Category ---
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    name: str
    items: List[ItemResponse] = []
    
    class Config:
        from_attributes = True