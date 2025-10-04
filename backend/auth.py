"""
@Author: Max Henson
@Version: 1.0
@Since: 10/3/2025

Usage:
    Provides authentication and security utilities for the backend.
    Includes functions for:
        • Password hashing and verification (using Passlib)
        • JWT token creation and decoding
        • Session expiration handling
        • User authentication support for protected routes

Change Log:
    Version 1.0 (10/3/2025): Implemented core authentication utilities and JWT support
"""




# auth.py - simple auth helpers (password hashing + simple token)
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days for dev

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_delta: int = None) -> str:
    expire = datetime.utcnow() + timedelta(minutes=(expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "exp": expire.isoformat()}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

