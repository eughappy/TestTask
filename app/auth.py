from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings
import redis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def store_token_in_redis(username: str, token: str, expiration: int = 3600):
    redis_client.setex(username, expiration, token)

def get_token_from_redis(username: str):
    return redis_client.get(username)
