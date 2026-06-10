import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from db import get_connection

HOST = 'localhost'
PORT = 8001


def serialize_note(row):
    return {
        "id": row[0],
        "title": row[1],
        "body": row[2],
        "tags": row[3],
        "created_at": row[4].isoformat(),
    }


def validate_note_payload(payload):
    title = payload.get("title", "").strip()
    body = payload.get("body", "").strip()
    tags = payload.get("tags", [])

    if not title:
        return None, "Title is required"

    if not body:
        return None, "Body is required"

    if not isinstance(tags, list):
        return None, "Tags must be a list"

    if not all(isinstance(tag, str) for tag in tags):
        return None, "Each tag must be a string"

    cleaned_note = {
        "title": title,
        "body": body,
        "tags": tags,
    }

    return cleaned_note, None


def parse_note_id(path):
    note_id_text = path.removeprefix('/notes/')

    try:
        return int(note_id_text)
    except ValueError:
        return None


class NotesHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/notes":
            query_params = parse_qs(parsed_url.query)
            search_query = query_params.get("q", [""])[0]
            self.handle_get_notes(search_query)
            return

        self.send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        if self.path == '/notes':
            self.handle_create_note()
            return
        self.send_json({'error': 'Not Found'}, status=404)

    def do_DELETE(self):
        if self.path.startswith('/notes/'):
            self.handle_delete_note()
            return
        self.send_json({'error': 'Not Found'}, status=404)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()
        
    
    def handle_get_notes(self, search_query=""):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                if search_query:
                    search_pattern = f"%{search_query}%"
                    cursor.execute(
                        """
                        SELECT id, title, body, tags, created_at
                        FROM notes
                        WHERE title ILIKE %s
                        OR body ILIKE %s
                        OR EXISTS (
                            SELECT 1
                            FROM unnest(tags) AS tag
                            WHERE tag ILIKE %s
                        )
                        ORDER BY created_at DESC;
                        """,
                        (search_pattern, search_pattern, search_pattern),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT id, title, body, tags, created_at
                        FROM notes
                        ORDER BY created_at DESC;
                        """
                    )

                rows = cursor.fetchall()

        notes = [serialize_note(row) for row in rows]

        self.send_json(notes)

    def handle_create_note(self):
        # First read — prepares the payload
        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length)
        body_text = body_bytes.decode("utf-8")

        # Tries to set the request body into the payload var
        try:
            payload = json.loads(body_text)
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON"}, status=400)
            return

        cleaned_note, validation_error = validate_note_payload(payload)

        if validation_error:
            self.send_json({"error": validation_error}, status=400)
            return
        
        # Upon validating the content, connects to Postgres and inserts the entry.
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO notes (title, body, tags)
                    VALUES (%s, %s, %s)
                    RETURNING id, title, body, tags, created_at;
                    """,
                    (
                        cleaned_note["title"],
                        cleaned_note["body"],
                        cleaned_note["tags"],
                    ),
                )
                row = cursor.fetchone()

        note = serialize_note(row)

        self.send_json(note, status=201)

    def handle_delete_note(self):
        note_id = parse_note_id(self.path)

        if note_id is None:
            self.send_json({'error': 'Invalid note id'}, status=400)
            return

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""DELETE from notes WHERE id = %s RETURNING id;""", (note_id,),)
                deleted_row = cursor.fetchone()
        
        if deleted_row is None:
            self.send_json({"error": "Note not found"}, status=404)
            return

        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def send_json(self, data, status=200):
        response_body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(response_body)

def run_server():
    server = HTTPServer((HOST, PORT), NotesHandler)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == '__main__':
    run_server()
