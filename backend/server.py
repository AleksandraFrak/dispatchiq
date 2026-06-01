from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "backend" / "dispatchiq.db"
HOST = "127.0.0.1"
PORT = 8000
PRIORITIES = {"Krytyczny", "Wysoki", "Średni", "Niski"}
STATUSES = {"Oczekuje", "Przyjęte", "W drodze", "Na miejscu", "Zamknięte"}


INCIDENTS = [
    ("ZGL-1024", "Nagły ból w klatce piersiowej", "Krytyczny", "Śródmieście", "ZRM-01", "W drodze", 4),
    ("ZGL-1025", "Wypadek komunikacyjny", "Wysoki", "Czuby", "ZRM-03", "Na miejscu", 0),
    ("ZGL-1026", "Utrata przytomności", "Krytyczny", "Kalinowszczyzna", "ZRM-02", "W drodze", 6),
    ("ZGL-1027", "Złamanie kończyny", "Średni", "LSM", "ZRM-07", "Przyjęte", 11),
    ("ZGL-1028", "Duszność", "Wysoki", "Wrotków", "ZRM-04", "W drodze", 5),
    ("ZGL-1029", "Gorączka u dziecka", "Niski", "Ponikwoda", "ZRM-08", "Oczekuje", 18),
    ("ZGL-1030", "Podejrzenie udaru", "Krytyczny", "Tatary", "ZRM-05", "W drodze", 3),
    ("ZGL-1031", "Zasłabnięcie", "Średni", "Bronowice", "ZRM-06", "Przyjęte", 9),
    ("ZGL-1032", "Reakcja alergiczna", "Wysoki", "Sławin", "ZRM-09", "W drodze", 7),
    ("ZGL-1033", "Uraz głowy", "Wysoki", "Felin", "ZRM-10", "Na miejscu", 0),
]


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                district TEXT NOT NULL,
                unit TEXT NOT NULL,
                status TEXT NOT NULL,
                eta_minutes INTEGER NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO incidents
                (code, title, priority, district, unit, status, eta_minutes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            INCIDENTS,
        )


def row_to_dict(row):
    return dict(row) if row else None


def parse_incident_id(path):
    prefix = "/api/incidents/"
    if not path.startswith(prefix):
        return None

    try:
        return int(path.removeprefix(prefix))
    except ValueError:
        return None


def validate_incident(data):
    errors = []
    required_fields = ["code", "title", "priority", "district", "unit", "status", "eta_minutes"]

    for field in required_fields:
        if field not in data or data[field] in ("", None):
            errors.append(f"Pole '{field}' jest wymagane.")

    if data.get("priority") and data["priority"] not in PRIORITIES:
        errors.append("Nieprawidłowy priorytet zgłoszenia.")

    if data.get("status") and data["status"] not in STATUSES:
        errors.append("Nieprawidłowy status zgłoszenia.")

    try:
        eta_minutes = int(data.get("eta_minutes", 0))
        if eta_minutes < 0:
            errors.append("ETA nie może być ujemne.")
    except (TypeError, ValueError):
        errors.append("ETA musi być liczbą.")

    return errors


class DispatchIQHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/incidents":
            self.send_incidents()
            return

        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/incidents":
            self.create_incident()
            return

        self.send_error_response(404, "Nie znaleziono endpointu.")

    def do_PUT(self):
        incident_id = parse_incident_id(urlparse(self.path).path)
        if incident_id:
            self.update_incident(incident_id)
            return

        self.send_error_response(404, "Nie znaleziono zgłoszenia.")

    def do_DELETE(self):
        incident_id = parse_incident_id(urlparse(self.path).path)
        if incident_id:
            self.delete_incident(incident_id)
            return

        self.send_error_response(404, "Nie znaleziono zgłoszenia.")

    def read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}

        body = self.rfile.read(content_length)
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def send_json_response(self, data, status=200):
        response = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def send_error_response(self, status, message):
        self.send_json_response({"error": message}, status)

    def send_incidents(self):
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, code, title, priority, district, unit, status, eta_minutes
                FROM incidents
                ORDER BY
                    CASE priority
                        WHEN 'Krytyczny' THEN 1
                        WHEN 'Wysoki' THEN 2
                        WHEN 'Średni' THEN 3
                        ELSE 4
                    END,
                    id ASC
                """
            ).fetchall()

        self.send_json_response([row_to_dict(row) for row in rows])

    def create_incident(self):
        data = self.read_json_body()
        if data is None:
            self.send_error_response(400, "Nieprawidłowy JSON.")
            return

        errors = validate_incident(data)
        if errors:
            self.send_json_response({"errors": errors}, 400)
            return

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO incidents
                        (code, title, priority, district, unit, status, eta_minutes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        data["code"].strip(),
                        data["title"].strip(),
                        data["priority"],
                        data["district"].strip(),
                        data["unit"].strip(),
                        data["status"],
                        int(data["eta_minutes"]),
                    ),
                )
                row = connection.execute(
                    """
                    SELECT id, code, title, priority, district, unit, status, eta_minutes
                    FROM incidents
                    WHERE id = ?
                    """,
                    (cursor.lastrowid,),
                ).fetchone()
        except sqlite3.IntegrityError:
            self.send_error_response(409, "Zgłoszenie z takim kodem już istnieje.")
            return

        self.send_json_response(row_to_dict(row), 201)

    def update_incident(self, incident_id):
        data = self.read_json_body()
        if data is None:
            self.send_error_response(400, "Nieprawidłowy JSON.")
            return

        errors = validate_incident(data)
        if errors:
            self.send_json_response({"errors": errors}, 400)
            return

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    """
                    UPDATE incidents
                    SET code = ?,
                        title = ?,
                        priority = ?,
                        district = ?,
                        unit = ?,
                        status = ?,
                        eta_minutes = ?
                    WHERE id = ?
                    """,
                    (
                        data["code"].strip(),
                        data["title"].strip(),
                        data["priority"],
                        data["district"].strip(),
                        data["unit"].strip(),
                        data["status"],
                        int(data["eta_minutes"]),
                        incident_id,
                    ),
                )
                if cursor.rowcount == 0:
                    self.send_error_response(404, "Nie znaleziono zgłoszenia.")
                    return

                row = connection.execute(
                    """
                    SELECT id, code, title, priority, district, unit, status, eta_minutes
                    FROM incidents
                    WHERE id = ?
                    """,
                    (incident_id,),
                ).fetchone()
        except sqlite3.IntegrityError:
            self.send_error_response(409, "Zgłoszenie z takim kodem już istnieje.")
            return

        self.send_json_response(row_to_dict(row))

    def delete_incident(self, incident_id):
        with get_connection() as connection:
            cursor = connection.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))

        if cursor.rowcount == 0:
            self.send_error_response(404, "Nie znaleziono zgłoszenia.")
            return

        self.send_json_response({"deleted": True, "id": incident_id})


class ReusableThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    initialize_database()
    server = ReusableThreadingHTTPServer((HOST, PORT), DispatchIQHandler)
    print(f"DispatchIQ backend działa: http://{HOST}:{PORT}")
    print(f"Endpoint API: http://{HOST}:{PORT}/api/incidents")
    server.serve_forever()
