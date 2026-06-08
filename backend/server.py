import json
from http.server import BaseHTTPRequestHandler, HTTPSServer, HTTPServer
from db import get_connection

HOST = 'localhost'
PORT = 8000

class NotesHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/notes':
            self.handle_get_notes()
            return
        self.send_json({'error': 'NotFound'}, status=404)

    def do_POST(self):
        if self.path == '/notes':
            self.handle_create_note()
            return
        self.send_json({'error': 'Not Found'}, status=404)
    
    def handle_get_notes(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, title, body, tags, created_at FROM notes ORDER BY created_at DESC;')
                rows = cursor.fetchall()
        
        notes = []
        for row in rows:
            note = {
                'id': row[0],
                'title': row[1],
                'body': row[2],
                'tags': row[3],
                'created_at': row[4].isoformat(),
            }
            notes.append(note)
        
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

        # Fields validation.
        title = payload.get("title", "").strip()
        body = payload.get("body", "").strip()
        tags = payload.get("tags", [])

        if not title:
            self.send_json({"error": "Title is required"}, status=400)
            return

        if not body:
            self.send_json({"error": "Body is required"}, status=400)
            return

        if not isinstance(tags, list):
            self.send_json({"error": "Tags must be a list"}, status=400)
            return
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO notes (title, body, tags)
                    VALUES (%s, %s, %s)
                    RETURNING id, title, body, tags, created_at;
                    """,
                    (title, body, tags),
                )
                row = cursor.fetchone()

        note = {
            "id": row[0],
            "title": row[1],
            "body": row[2],
            "tags": row[3],
            "created_at": row[4].isoformat(),
        }

        self.send_json(note, status=201)

    def send_json(self, data, status=200):
        response_body = json.dumps(data).encode('utf-8')

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response_body)

def run_server():
    server = HTTPServer((HOST, PORT), NotesHandler)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == '__main__':
    run_server()