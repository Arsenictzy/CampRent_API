from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    name: str
    stock: int

class ItemCreate(ItemBase):
    category_id: int

class Item(ItemBase):
    id: int
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    id: int
    items: List[Item] = []
    class Config:
        orm_mode = True