from fastapi import FastAPI

from api import routes
from celery_tasks.task import data_extraction

app = FastAPI()

app.include_router(routes.router)

data_extraction.delay()