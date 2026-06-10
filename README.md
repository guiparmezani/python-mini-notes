# Python Notes

Python Notes is a small full-stack notes app built as a learning project for Python, HTTP APIs, PostgreSQL, Docker, and React.

The first backend intentionally uses Python's built-in `http.server` instead of a framework. The goal is to understand the mechanics that frameworks usually hide: routing, request parsing, JSON responses, CORS, SQL queries, and database connections.

## Stack

- Backend: Python, `http.server`, `psycopg`, `python-dotenv`
- Frontend: React, TypeScript, Vite
- Database: PostgreSQL 16
- Local services: Docker Compose

## Project Layout

```text
backend/                 Python API server
frontend/                React/Vite frontend
docs/                    Project specs and notes
docker-compose.yml       PostgreSQL service
requirements.txt         Python dependencies
```

## Requirements

- Python 3
- Node.js and npm
- Docker Desktop or Docker Engine with Compose

## Environment

Create a root `.env` file for the Python backend:

```env
DATABASE_URL=postgresql://notes_app:notes_app@localhost:55432/notes_app
```

Create `frontend/.env` for the React app:

```env
VITE_API_BASE_URL=http://localhost:8001
```

## Setup

Create and activate the Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start PostgreSQL:

```bash
docker compose up -d
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

## Database

Connect to Postgres:

```bash
docker compose exec postgres psql -U notes_app -d notes_app
```

Create the notes table if it does not exist:

```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);
```

Exit `psql`:

```sql
\q
```

## Running The App

Run the backend from the project root:

```bash
source .venv/bin/activate
python backend/server.py
```

The backend runs at:

```text
http://localhost:8001
```

Run the frontend in a second terminal:

```bash
cd frontend
npm run dev
```

Vite prints the frontend URL, usually:

```text
http://localhost:5173
```

## API Endpoints

List notes:

```http
GET /notes
```

Search notes:

```http
GET /notes?q=python
```

Create a note:

```http
POST /notes
Content-Type: application/json
```

```json
{
  "title": "Study Python",
  "body": "Practice request parsing and SQL",
  "tags": ["python", "api"]
}
```

Delete a note:

```http
DELETE /notes/1
```

## Useful Commands

Check running Docker services:

```bash
docker compose ps
```

View Postgres logs:

```bash
docker compose logs postgres
```

Stop services:

```bash
docker compose down
```

Freeze Python dependencies after adding packages:

```bash
python -m pip freeze > requirements.txt
```

Build the frontend:

```bash
cd frontend
npm run build
```

## Learning Goals

This project is meant to build comfort with:

- Python virtual environments and dependencies
- HTTP request handlers
- JSON request/response handling
- SQL and PostgreSQL CRUD operations
- Docker Compose service management
- React state, forms, effects, and fetch calls
- Frontend/backend integration and CORS

The goal is not production architecture. A later project can use Django and Django REST Framework to practice the framework patterns used in larger Python applications.
