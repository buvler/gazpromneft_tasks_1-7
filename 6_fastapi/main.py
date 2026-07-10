from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="User Management API",
    description="Простой CRUD API для управления пользователями",
    version="1.0.0"
)

users_db = []
current_id = 1

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class User(BaseModel):
    id: int
    name: str
    email: str


@app.post("/users/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    """Создать нового пользователя."""
    global current_id
    
    new_user = User(id=current_id, **user.dict())
    users_db.append(new_user)
    
    current_id += 1
    return new_user

@app.get("/users/", response_model=List[User])
def read_users():
    """Получить список всех пользователей."""
    return users_db

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    """Получить данные конкретного пользователя по ID."""
    for user in users_db:
        if user.id == user_id:
            return user
            
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Обновить данные пользователя (полностью или частично)."""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            user_data = user.dict()
            update_data = user_update.dict(exclude_unset=True)
            
            user_data.update(update_data)
            updated_user = User(**user_data)
            users_db[i] = updated_user
            
            return updated_user
            
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    """Удалить пользователя по ID."""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[i]
            return # 204 No Content не требует возврата тела ответа
            
    raise HTTPException(status_code=404, detail="Пользователь не найден")