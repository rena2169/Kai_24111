from pydantic import BaseModel
from typing import Optional

# То, что присылает пользователь при создании
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

# То, что присылает пользователь при обновлении (все поля необязательны)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# То, что API возвращает пользователю (добавляем id)
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True # Позволяет читать данные из объектов БД

# Здесь мы описываем, какие данные принимает и отдает API. Это защищает от мусора (например, если вместо строки пришлют число).