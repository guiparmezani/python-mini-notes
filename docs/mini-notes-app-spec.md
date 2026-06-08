# Mini Notes App (React + Python + PostgreSQL)

## Goal

Build a very small full-stack application to practice:

- React fundamentals
- Python fundamentals
- REST API design
- PostgreSQL integration
- Docker-based local services
- Frontend/backend communication
- Loading and error states
- Basic CRUD operations

This project is intentionally small enough to complete in a few hours.

---

## Tech Stack

### Frontend

- React
- Vite
- TypeScript (optional but recommended)
- Fetch API
- No UI framework required

### Backend

- Python
- Built-in `http.server`
- `psycopg` (PostgreSQL driver)
- `python-dotenv`
- Local Python virtual environment for the first implementation

### Database

- PostgreSQL 16
- Run through Docker Compose

### Infrastructure / Local Services

- Docker
- Docker Compose
- PostgreSQL container
- Optional later: containerize the backend after the raw Python version works locally

### Docker Usage Policy

Use Docker for services that would otherwise require machine-level installation or long-lived local setup.

For this app:

- Run PostgreSQL in Docker Compose.
- Keep the Python backend in a local virtual environment at first, so Python imports, scripts, packages, and debugging stay visible.
- Keep the React frontend local through Vite at first.
- Add backend/frontend containers only as a later Docker learning step, after the app works locally.

This keeps Docker in the workflow without hiding the Python concepts this project is meant to teach.

---

## Local Development Setup

### Python Environment

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install "psycopg[binary]" python-dotenv
python -m pip freeze > requirements.txt
```

### Docker Compose Services

Create a `docker-compose.yml` with PostgreSQL:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: notes_app
      POSTGRES_USER: notes_app
      POSTGRES_PASSWORD: notes_app
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Start the database:

```bash
docker compose up -d
```

The backend should connect to:

```env
DATABASE_URL=postgresql://notes_app:notes_app@localhost:5432/notes_app
```

Use `localhost` because Docker maps the container's PostgreSQL port to the host machine.

---

## Database Schema

```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Endpoints

### Get all notes

```http
GET /notes
```

Response:

```json
[
  {
    "id": 1,
    "title": "Study React",
    "body": "Review useEffect and state management",
    "tags": ["react", "hooks"],
    "created_at": "2026-06-03T12:00:00"
  }
]
```

---

### Create a note

```http
POST /notes
```

Request:

```json
{
  "title": "Study Python",
  "body": "Review classes and generators",
  "tags": ["python"]
}
```

---

### Delete a note

```http
DELETE /notes/1
```

---

### Optional Search

```http
GET /notes?q=react
```

Search title, body, or tags.

---

## Python Dependencies

Install:

```bash
python -m pip install "psycopg[binary]" python-dotenv
```

---

## Backend Requirements

### Responsibilities

- Connect to PostgreSQL
- Return JSON responses
- Parse JSON request bodies
- Handle CORS headers
- Perform CRUD operations
- Return proper HTTP status codes

### Practice Topics

- HTTP methods
- Routing
- Request parsing
- Response serialization
- Database connections
- SQL queries
- Error handling
- Environment variables
- Virtual environments

---

## Frontend Requirements

### Pages

Single-page application.

### Features

#### Notes List

- Display all notes
- Show title
- Show body
- Show tags
- Show creation date

#### Create Note Form

Fields:

- Title
- Body
- Tags (comma-separated)

Validation:

- Title required
- Body required

#### Delete Note

- Delete from database
- Refresh UI

#### Search

- Filter notes
- Call backend search endpoint

---

## React Practice Topics

### State

Practice:

- useState
- useEffect

### API Communication

Practice:

- fetch()
- async/await
- Loading states
- Error states

### Rendering

Practice:

- Lists
- Conditional rendering
- Forms
- Controlled inputs

---

## Suggested Build Order

### Phase 0

Prepare the local development environment.

Implement:

- Create `.venv`
- Install Python dependencies
- Create `.env`
- Create `.gitignore`
- Create `docker-compose.yml`

### Phase 1

Start PostgreSQL with Docker Compose and create the database table.

Implement:

- `docker compose up -d`
- Verify the database container is running
- Connect to PostgreSQL
- Create the `notes` table

### Phase 2

Create Python server.

Implement:

- GET /notes
- POST /notes
- DELETE /notes/:id

Verify using Postman or curl.

### Phase 3

Create React app with Vite.

Display notes from API.

### Phase 4

Create note form.

Save notes through backend.

### Phase 5

Implement delete functionality.

### Phase 6

Implement search.

### Phase 7

Polish UI.

Add:

- Loading state
- Error state
- Empty state
- Tag badges

### Phase 8

Optional Docker learning step.

Add:

- Backend `Dockerfile`
- Backend service in `docker-compose.yml`
- Frontend service in `docker-compose.yml`
- Internal Docker networking between services

Only do this after the app already works locally with Python running from `.venv`.

---

## Success Criteria

By the end of the project you should be comfortable with:

- React state management
- React forms
- React API calls
- Python HTTP handling
- PostgreSQL CRUD operations
- Docker Compose service management
- Environment-based configuration
- JSON APIs
- Frontend/backend integration

The goal is not to build a production application.

The goal is to become sharper with React, Python, SQL, Docker, APIs, and debugging before technical interviews.
