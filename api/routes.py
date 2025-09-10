from typing import Dict

from fastapi import APIRouter, HTTPException, status

from api.schemas import (CreateTaskSchema,
                         UpdateTaskSchema,
                         ResponseTaskSchema,
                         PredictionRequestSchema,
                         PredictionResponseSchema)
from model import tokinize_sentese
from joblib import load

router = APIRouter()
ml_model = load("./model.joblib")

id_count = 1
db: Dict[int, dict] = {}


@router.get(
    "/tasks",
    response_model=list[ResponseTaskSchema],
    status_code=status.HTTP_200_OK,
    summary="Gives as the entire list of tasks",
    description="Get a list all our task with id, title,\
                description, completed status (true, false)"
)
def get_tasks():
    return list(db.values())


@router.post(
    "/tasks",
    response_model=ResponseTaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task",
    description="Create a new task with filds:\
                title (required string field)\
                description (optional string field)\
                completed (oprional bool field, false by default)"
)
def create_task(task: CreateTaskSchema):
    global id_count
    id_count += 1

    new_task = {"id": id_count, **task.model_dump()}
    db[id_count] = new_task

    return new_task


@router.put(
    "/tasks/{id}",
    response_model=ResponseTaskSchema,
    status_code=status.HTTP_200_OK,
    summary="Upadte task by id",
    description="Update all filds what you want, remind the restrictions\
                title (required string field)\
                description (optional string field)\
                completed (oprional bool field, false by default)"
)
def update_task(id: int, update: UpdateTaskSchema):
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found")

    task = ResponseTaskSchema.model_validate(db[id])
    data = update.model_dump(exclude_unset=True)
    updated_task = task.model_copy(update=data)
    db[id] = updated_task

    return updated_task


@router.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task by id",
    description="Delete task by id, I don't know what to add"
)
def delete_task(id: int):
    if id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    
    del db[id]

    return {"message": "Deleted successfuly"}


@router.post(
    "/prediction",
    response_model=PredictionResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Predict how importent task"
)
def prediction(task: PredictionRequestSchema):
    task_string = task.task_description
    prediction = ml_model.predict([task_string])
    return {"prediction": prediction[0]}
