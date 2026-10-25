from fastapi import FastAPI, HTTPException
from typing import List
from database import Base, SessionLocal, engine
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse

Base.metadata.create_all(bind=engine)  # Создаем таблицу, если её нет
app = FastAPI(title="To-Do List API")


# 1. CREATE: Создать задачу (POST)
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    db = SessionLocal()
    new_task = Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)  # Чтобы получить id из БД
    db.close()
    return new_task


# 2. READ (All): Получить все задачи (GET)
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return tasks


# 3. READ (One): Получить одну задачу по ID (GET)
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    db.close()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


# 4. UPDATE: Обновить задачу (PUT)
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # Обновляем только те поля, которые пришли
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    db.commit()
    db.refresh(task)
    db.close()
    return task


# 5. DELETE: Удалить задачу (DELETE)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Задача не найдена")

    db.delete(task)
    db.commit()
    db.close()
    return {"message": "Задача удалена"}