from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Task(Base):
    __tablename__ = "tasks"  # Имя таблицы в БД

    id = Column(Integer, primary_key=True, index=True)  # Уникальный номер
    title = Column(String, index=True)  # Заголовок
    description = Column(String, nullable=True)  # Описание (может быть пустым)
    completed = Column(Boolean, default=False)  # Статус (по умолчанию False)

# Здесь мы описываем класс, который SQLAlchemy превратит в таблицу.