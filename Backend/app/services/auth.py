import sqlite3
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, constr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "your-secure-secret-key-here")  # Ensure .env has a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///kura_kani.db")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def init_db():
    """Initialize the SQLite database and create the users table."""
    with sqlite3.connect(DATABASE_URL.replace("sqlite:///", "")) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

init_db()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Create a JWT access token with expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Retrieve the current user from a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    """Register a new user and return a JWT token."""
    with sqlite3.connect(DATABASE_URL.replace("sqlite:///", "")) as conn:
        cursor = conn.cursor()
        try:
            hashed_password = hash_password(user.password)
            cursor.execute(
                "INSERT INTO users (username, hashed_password, email) VALUES (?, ?, ?)",
                (user.username, hashed_password, user.email)
            )
            conn.commit()
            access_token = create_access_token(data={"sub": user.username})
            return {"access_token": access_token, "token_type": "bearer"}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Username or email already exists")

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate a user and return a JWT token."""
    with sqlite3.connect(DATABASE_URL.replace("sqlite:///", "")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, hashed_password FROM users WHERE username = ?", (form_data.username,))
        user = cursor.fetchone()
        if not user or not verify_password(form_data.password, user[1]):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": user[0]})
        return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    """Return the current user's information."""
    return {"username": current_user}

@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    """Example of a protected route requiring authentication."""
    return {"message": f"Hello, {current_user}! This is a protected route."}