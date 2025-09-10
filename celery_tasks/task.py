from csv import DictWriter
import requests

from celery import Celery
from requests.exceptions import RequestException

app = Celery(main="celery_tasks.task", broker="redis://redis:6379")
url = "https://jsonplaceholder.typicode.com/users"
fieldnames = ["id", "name", "email"]


@app.task
def data_extraction():
    try:
        response = requests.get(url=url)
        data = response.json()
    except RequestException as e:
        print(f"Request failure {e}")
    with open("./data.csv", "w", newline="", encoding="utf-8") as file:
        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([{"id": d["id"], "name": d["name"], "email": d["email"]} for d in data])
