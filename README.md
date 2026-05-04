# Project Portfolio

REST API for managing a developer project portfolio. Built with Flask + SQLAlchemy, Python 3.11.3.

## Stack

- **Backend:** Python 3.11, Flask, Flask-Smorest, SQLAlchemy
- **Database:** PostgreSQL (Docker) / SQLite (local)
- **Migrations:** Alembic
- **Docs:** Swagger UI — `/docs`

## Getting started

### Local

```bash
cd backend
pip install -r requirements.txt
flask --app api/app.py run
```

### Docker

```bash
# create .env file
echo "POSTGRES_PASSWORD=secret\nAPI_KEY=your-key" > .env

docker compose up --build
```

On startup the container automatically runs `alembic upgrade head`.

## Environment variables

| Variable | Description |
|---|---|
| `API_KEY` | API key for Bearer auth |
| `POSTGRES_PASSWORD` | PostgreSQL password (Docker only) |

## Authentication

All requests require a Bearer token:

```
Authorization: Bearer <API_KEY>
```

## API

Base path: `/api`

| Method | Path | Description |
|---|---|---|
| GET | `/projects` | List projects |
| GET | `/projects/<id>` | Get project by ID |
| POST | `/projects` | Create project |
| DELETE | `/projects/<id>` | Delete project |

### GET /api/projects — query parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | Page number |
| `per_page` | int | 10 | Items per page (max 100) |
| `search` | string | — | Search by name or description |
| `technology` | string[] | — | Filter by technology (repeatable) |
| `sort_by` | string | `id` | Sort field: `id`, `name`, `start_date`, `end_date` |
| `order` | string | `asc` | Sort order: `asc`, `desc` |

### POST /api/projects — request body

```json
{
  "name": "My Project",
  "description": "Project description",
  "technologies": ["Python", "React"],
  "start_date": "2024-01-01",
  "end_date": null
}
```

## Seed data

```bash
docker compose exec app python -m db.seed
```

## Tests

```bash
cd backend
pytest tests/
```

## Health check

```
GET /api/health
```

Returns `{ "status": "ok", "db": "ok" }`.
