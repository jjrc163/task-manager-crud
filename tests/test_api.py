import pytest

import app as app_module
from db import TaskStore


@pytest.fixture
def client(tmp_path, monkeypatch):
    store = TaskStore(tmp_path / "test.db")
    monkeypatch.setattr(app_module, "store", store)
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_list_is_empty_initially(client):
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert res.get_json() == []


def test_create_and_list(client):
    res = client.post("/api/tasks", json={"title": "Write tests"})
    assert res.status_code == 201
    task = res.get_json()
    assert task["title"] == "Write tests"
    assert task["done"] is False

    listed = client.get("/api/tasks").get_json()
    assert len(listed) == 1


def test_create_rejects_empty_title(client):
    res = client.post("/api/tasks", json={"title": "   "})
    assert res.status_code == 400


def test_update_toggles_done(client):
    task_id = client.post("/api/tasks", json={"title": "Ship it"}).get_json()["id"]
    res = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True


def test_get_missing_task_returns_404(client):
    assert client.get("/api/tasks/999").status_code == 404


def test_delete_task(client):
    task_id = client.post("/api/tasks", json={"title": "Temp"}).get_json()["id"]
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get(f"/api/tasks/{task_id}").status_code == 404


def test_store_persists_across_instances(tmp_path):
    path = tmp_path / "persist.db"
    TaskStore(path).create("Persisted")
    assert TaskStore(path).list()[0]["title"] == "Persisted"