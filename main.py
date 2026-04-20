from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

# Import internal proyek
import database
from models import user as user_models
from models import item as item_models
from schemas import item_schema as schemas
from routers import item_router
from auth import security

# Inisialisasi Tabel Database secara otomatis saat startup
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="CampRent API - Sistem Sewa Alat Camping",
    description="API untuk mengelola inventaris alat outdoor dengan autentikasi JWT",
    version="1.0.0"
)

# --- Endpoint Registrasi (Wajib) ---
@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Cek apakah username sudah ada
    db_user = db.query(user_models.User).filter(user_models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terdaftar")
    
    hashed_password = security.hash_password(user.password)
    new_user = user_models.User(username=user.username, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User berhasil didaftarkan"}

# --- Endpoint Login untuk Mendapatkan Token JWT (Wajib) ---
@app.post("/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(user_models.User).filter(user_models.User.username == form_data.username).first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Menghubungkan Router Modular ---
app.include_router(item_router.router)

# Endpoint Root untuk pengecekan awal
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Selamat datang di CampRent API",
        "docs": "/docs",
        "status": "Running"
    }