from db import get_connection

def main():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, title, body, tags, created_at FROM notes;')
            rows = cursor.fetchall()
    print(rows)

if __name__ == '__main__':
    main()