# Mini Notes App (React + Python + PostgreSQL)

## Goal

Build a very small full-stack application to practice:

- React fundamentals
- Python fundamentals
- REST API design
- PostgreSQL integration
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

### Database

- PostgreSQL

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
pip install psycopg[binary] python-dotenv
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

### Phase 1

Create PostgreSQL database and table.

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

---

## Success Criteria

By the end of the project you should be comfortable with:

- React state management
- React forms
- React API calls
- Python HTTP handling
- PostgreSQL CRUD operations
- JSON APIs
- Frontend/backend integration

The goal is not to build a production application.

The goal is to become sharper with React, Python, SQL, APIs, and debugging before technical interviews.
