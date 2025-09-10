from pydantic import BaseModel
from typing import Optional


class CreateTaskSchema(BaseModel):
    title: str
    completed: Optional[bool] = False
    description: Optional[str] = None


class UpdateTaskSchema(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    description: Optional[str] = None

class ResponseTaskSchema(BaseModel):
    id: int
    title: str
    completed: Optional[bool] = False
    description: Optional[str] = None

class PredictionRequestSchema(BaseModel):
    task_description: str

class PredictionResponseSchema(BaseModel):
    prediction: str