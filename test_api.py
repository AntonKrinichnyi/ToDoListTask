import unittest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

response = client.get("/")

class TestAPI(unittest.TestCase):
    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_create_item(self):
        data = {"title": "Test task", "description": "A test task"}
        response = client.post("/tasks/", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Test Item")

    def test_get_item(self):
        data = {"title": "Get some task", "description": "Some task"}
        post_response = client.post("/tasks/", json=data)

        task_id = post_response.json()["id"]
        get_response = client.get(f"/tasks/{task_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["task"], "Get some task")

    def test_update_item(self):
        data = {"title": "Update task", "description": "To update my task"}
        post_response = client.post("/tasks/", json=data)
        task_id = post_response.json()["id"]

        update_data = {"title": "Updated", "completed": True}
        put_response = client.put(f"/tasks/{task_id}", json=update_data)
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json()["title"], "Updated")

    def test_delete_item(self):

        data = {"title": "Delete Item"}
        post_response = client.post("/tasks/", json=data)
        task_id = post_response.json()["id"]

        delete_response = client.delete(f"/tasks/{task_id}")
        self.assertEqual(delete_response.status_code, 204)

        get_response = client.get(f"/tasks/{task_id}")
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()