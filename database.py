from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///tasks.db") # Файл базы создастся сам
Base = declarative_base() # Базовый класс для моделей
SessionLocal = sessionmaker(bind=engine) # Фабрика сессий для запросов

# Здесь мы говорим Python, где хранить данные (в файле tasks.db).