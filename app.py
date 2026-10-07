"""A small task manager: REST API + web UI backed by SQLite.

Endpoints:
    GET    /api/tasks          list tasks
    POST   /api/tasks          create a task        {"title": "..."}
    GET    /api/tasks/<id>     fetch one task
    PATCH  /api/tasks/<id>     update a task        {"title"?, "done"?}
    DELETE /api/tasks/<id>     delete a task
"""
from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request

from db import TaskStore

app = Flask(__name__)
store = TaskStore(os.getenv("TASKS_DB", "tasks.db"))


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/tasks")
def list_tasks():
    return jsonify(store.list())


@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    try:
        task = store.create(str(data.get("title", "")))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(task), 201


@app.get("/api/tasks/<int:task_id>")
def get_task(task_id: int):
    task = store.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found."}), 404
    return jsonify(task)


@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id: int):
    data = request.get_json(silent=True) or {}
    try:
        task = store.update(task_id, title=data.get("title"), done=data.get("done"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if task is None:
        return jsonify({"error": "Task not found."}), 404
    return jsonify(task)


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id: int):
    if not store.delete(task_id):
        return jsonify({"error": "Task not found."}), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)