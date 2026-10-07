"""SQLite persistence for tasks. Standard library only."""
from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT    NOT NULL,
    done       INTEGER NOT NULL DEFAULT 0,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""


class TaskStore:
    """A tiny data-access layer over a SQLite database."""

    def __init__(self, db_path: str | Path = "tasks.db") -> None:
        self.db_path = str(db_path)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_schema(self) -> None:
        with self._connect() as connection:
            connection.executescript(SCHEMA)

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict:
        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
            "created_at": row["created_at"],
        }

    def list(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM tasks ORDER BY done ASC, id DESC"
            ).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get(self, task_id: int) -> dict | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return self._row_to_dict(row) if row else None

    def create(self, title: str) -> dict:
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        with self._connect() as connection:
            cursor = connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            task_id = cursor.lastrowid
        return self.get(task_id)  # type: ignore[return-value]

    def update(self, task_id: int, title: str | None = None, done: bool | None = None) -> dict | None:
        current = self.get(task_id)
        if current is None:
            return None
        new_title = current["title"] if title is None else title.strip()
        if not new_title:
            raise ValueError("Title cannot be empty.")
        new_done = current["done"] if done is None else done
        with self._connect() as connection:
            connection.execute(
                "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
                (new_title, int(new_done), task_id),
            )
        return self.get(task_id)

    def delete(self, task_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cursor.rowcount > 0