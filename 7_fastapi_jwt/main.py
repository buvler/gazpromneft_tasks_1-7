import time
import hashlib
import jwt
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


SECRET_KEY = "my_super_secret_key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="JWT Auth API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

# In-memory хранилище (словарь: {username: hashed_password})
users_db = {}


def get_password_hash(password: str) -> str:
    """Хэширование пароля (в проде используйте passlib + bcrypt)."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка совпадения паролей."""
    return get_password_hash(plain_password) == hashed_password

def create_access_token(data: dict) -> str:
    """Генерация JWT токена."""
    to_encode = data.copy()
    expire = time.time() + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Зависимость (Dependency) для защиты маршрутов.
    Проверяет валидность токена и возвращает имя пользователя.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные (Неверный или просроченный токен)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истек")
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    if username not in users_db:
        raise credentials_exception
        
    return username


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    """Регистрация нового пользователя."""
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    users_db[user.username] = get_password_hash(user.password)
    return {"username": user.username}


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Вход и получение токена.
    Использует стандартную форму OAuth2 (передается через form-data, а не JSON).
    """
    if form_data.username not in users_db:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")
    
    hashed_pass = users_db[form_data.username]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")
    
    access_token = create_access_token(data={"sub": form_data.username})
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected", response_model=UserResponse)
def protected_route(current_user: str = Depends(get_current_user)):
    """
    Защищенный маршрут. 
    Требует валидный токен в заголовке Authorization: Bearer <token>.
    """
    return {"username": current_user}