from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "KEVIN_SECRET_CAMP" # Tetap gunakan secret key kamu
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# PERBAIKAN: Menambahkan parameter bcrypt__truncate_error untuk mengatasi error versi bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__truncate_error=True 
)

def hash_password(password: str):
    """Mengubah password plain text menjadi hash yang aman."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Memverifikasi apakah password input cocok dengan hash di database."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Membuat token JWT dengan masa berlaku 30 menit[cite: 81]."""
    to_encode = data.copy()
    # Gunakan timezone-aware UTC untuk menghindari warning di Python terbaru
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Fungsi proteksi endpoint (Dependency Injection) 
def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validasi token JWT untuk melindungi endpoint yang membutuhkan proteksi[cite: 32]."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token tidak valid"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token kadaluarsa atau salah"
        )