# task-manager-crud

A small **task manager** with a REST API and a web UI, backed by **SQLite**. Built with Flask and the Python standard library.

Demonstrates a clean separation between the HTTP layer (`app.py`) and the data layer (`db.py`), with full CRUD and a test suite.

## Features

- Full CRUD: create, list, read, update (toggle done), delete
- REST API returning JSON with proper status codes (`201`, `204`, `400`, `404`)
- Vanilla-JS frontend — no build step
- SQLite persistence via a small data-access layer
- Tested with pytest

## Quick start

```bash
git clone https://github.com/jjrc163/task-manager-crud.git
cd task-manager-crud
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

## API

| Method | Path | Body | Result |
|---|---|---|---|
| `GET` | `/api/tasks` | — | list of tasks |
| `POST` | `/api/tasks` | `{"title": "..."}` | `201` + task |
| `GET` | `/api/tasks/<id>` | — | task or `404` |
| `PATCH` | `/api/tasks/<id>` | `{"title"?, "done"?}` | updated task |
| `DELETE` | `/api/tasks/<id>` | — | `204` |

```bash
curl -X POST http://127.0.0.1:5000/api/tasks \
  -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

## Project layout

```
task-manager-crud/
├── app.py              # Flask routes (HTTP layer)
├── db.py               # SQLite data-access layer
├── templates/index.html
├── static/app.js
├── static/style.css
└── tests/test_api.py
```

## Tests

```bash
pip install -r requirements.txt
pytest -q
```

## Design notes

- **Layered.** Routes never touch SQL; the store never touches HTTP.
- **Safe writes.** Parameterized queries throughout (no string-built SQL).
- **Configurable.** Point `TASKS_DB` at any path to change the database file.

## License

MIT — see [LICENSE](LICENSE).