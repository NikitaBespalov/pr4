from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

app = FastAPI()


class LabTask(BaseModel):
    name: str = Field(..., description="Название лабораторной работы")
    due_date: date = Field(..., description="Крайний срок выполнения в формате: YYYY-MM-DD")
    notes: Optional[str] = Field(None, description="Дополнительная информация (необязательно)")
    participants: Optional[List[str]] = Field(default_factory=list, description="Список участников (необязательно)")


# Словарь для хранения данных о лабораторных работах
lab_storage = {}


@app.post("/tasks", status_code=201)
def create_lab_task(task: LabTask):
    if task.name in lab_storage:
        raise HTTPException(status_code=400, detail="Работа с указанным названием уже существует.")

    lab_storage[task.name] = task
    return {"resource": f"/tasks/{task.name}"}


@app.put("/tasks/{name}")
def modify_lab_task(name: str, updated_task: LabTask):
    if name not in lab_storage:
        raise HTTPException(status_code=404, detail="Запись с таким названием не найдена.")
    if updated_task.name != name:
        raise HTTPException(status_code=400, detail="Название работы менять нельзя.")

    lab_storage[name] = updated_task
    return {"status": "Обновление успешно выполнено."}


@app.delete("/tasks/{name}")
def remove_lab_task(name: str):
    if name not in lab_storage:
        raise HTTPException(status_code=404, detail="Лабораторная работа не найдена.")

    del lab_storage[name]
    return {"status": "Удаление успешно выполнено."}


@app.get("/tasks/{name}")
def retrieve_lab_task(name: str):
    if name not in lab_storage:
        raise HTTPException(status_code=404, detail="Данные по указанной работе отсутствуют.")

    return lab_storage[name]


@app.get("/tasks")
def list_all_lab_tasks():
    return list(lab_storage.values())
