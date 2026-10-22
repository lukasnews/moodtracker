#!/usr/bin/env python3
"""
Our Mood – minimaler Sync-Server (nur Python-Standardbibliothek).

Der Server speichert ausschließlich die im Browser verschlüsselten Daten (AES-256-GCM).
Er kennt weder euer Paar-Passwort noch den Schlüssel zum Entschlüsseln:
  - Die App leitet aus dem Passwort zwei getrennte Werte ab:
      1. einen Anmelde-Token (PBKDF2, fester App-Salt) → wird hier nur als SHA-256-Hash gespeichert
      2. den Verschlüsselungsschlüssel (PBKDF2, zufälliger Salt) → verlässt nie das Gerät
  - Fehlversuche werden pro IP und global gebremst.

Endpunkte (JSON):
  GET  /v1/health            → {"ok": true}
  GET  /v1/data              → {"version": n, "data": {...}} | 404 (noch leer) | 401
  PUT  /v1/data              ← {"version": erwartet, "data": {...}} → 200 | 409 (Konflikt) | 401
  POST /v1/rekey             ← {"newToken": "...", "version": erwartet, "data": {...}, "revokeOld": bool}
                               (Passwort ändern; mit revokeOld=true werden alle Geräte mit dem alten
                               Passwort abgemeldet: Sie erhalten 410 und löschen ihre lokalen Daten.)

Konfiguration über Umgebungsvariablen (siehe docker-compose.yml).
"""
import hashlib
import hmac
import json
import os
import re
import sqlite3
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_PATH = os.environ.get("DB_PATH", "/data/our-mood-sync.db")
PORT = int(os.environ.get("PORT", "8080"))
ALLOWED_ORIGINS = [o.strip().rstrip("/") for o in os.environ.get("ALLOWED_ORIGINS", "https://moods.chaoten.online").split(",") if o.strip()]
MAX_SPACES = int(os.environ.get("MAX_SPACES", "1"))           # 1 = genau ein Paar pro Server
MAX_BODY_BYTES = int(os.environ.get("MAX_BODY_BYTES", str(5 * 1024 * 1024)))
TRUST_PROXY = os.environ.get("TRUST_PROXY", "1") == "1"        # hinter Reverse Proxy / Cloudflare
FAILS_PER_IP = int(os.environ.get("FAILS_PER_IP", "10"))       # Fehlversuche pro IP …
FAIL_WINDOW = int(os.environ.get("FAIL_WINDOW_SECONDS", "900"))  # … in 15 Minuten
FAILS_GLOBAL = int(os.environ.get("FAILS_GLOBAL", "100"))      # Fehlversuche insgesamt pro Stunde

TOKEN_RE = re.compile(r"^[0-9a-f]{64}$")

db_lock = threading.Lock()
fail_lock = threading.Lock()
fails_by_ip = {}
fails_global = []


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def token_hash(token):
    return hashlib.sha256(token.encode("ascii")).hexdigest()


def open_db():
    directory = os.path.dirname(DB_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS spaces (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               token_hash TEXT NOT NULL UNIQUE,
               version INTEGER NOT NULL,
               data TEXT NOT NULL,
               created_at TEXT NOT NULL,
               updated_at TEXT NOT NULL
           )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS revoked (
               token_hash TEXT PRIMARY KEY,
               revoked_at TEXT NOT NULL
           )"""
    )
    conn.commit()
    return conn


DB = open_db()


def find_space(token):
    """Sucht den Bereich zum Token (zeitkonstanter Vergleich der Hashes)."""
    wanted = token_hash(token)
    with db_lock:
        rows = DB.execute("SELECT id, token_hash, version, data FROM spaces").fetchall()
    for row in rows:
        if hmac.compare_digest(row[1], wanted):
            return {"id": row[0], "version": row[2], "data": row[3]}
    return None


def is_revoked(token):
    with db_lock:
        return DB.execute("SELECT 1 FROM revoked WHERE token_hash = ?", (token_hash(token),)).fetchone() is not None


def space_count():
    with db_lock:
        return DB.execute("SELECT COUNT(*) FROM spaces").fetchone()[0]


def valid_envelope(data):
    """Nur das erwartete, verschlüsselte Format annehmen."""
    return (
        isinstance(data, dict)
        and data.get("app") == "Our Mood"
        and data.get("v") == 1
        and isinstance(data.get("ct"), str)
        and isinstance(data.get("iv"), str)
        and isinstance(data.get("salt"), str)
    )


class Handler(BaseHTTPRequestHandler):
    server_version = "OurMoodSync/1.0"
    sys_version = ""

    # ---------- Hilfsfunktionen ----------
    def client_ip(self):
        if TRUST_PROXY:
            cf = self.headers.get("CF-Connecting-IP")
            if cf:
                return cf.strip()
            xff = self.headers.get("X-Forwarded-For")
            if xff:
                return xff.split(",")[0].strip()
        return self.client_address[0]

    def cors_headers(self):
        origin = (self.headers.get("Origin") or "").rstrip("/")
        if origin and origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
            self.send_header("Access-Control-Max-Age", "600")

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY_BYTES:
            return None
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None

    def rate_limited(self):
        cutoff = time.time()
        with fail_lock:
            recent_ip = [t for t in fails_by_ip.get(self.client_ip(), []) if t > cutoff - FAIL_WINDOW]
            fails_by_ip[self.client_ip()] = recent_ip
            fails_global[:] = [t for t in fails_global if t > cutoff - 3600]
            return len(recent_ip) >= FAILS_PER_IP or len(fails_global) >= FAILS_GLOBAL

    def record_failure(self):
        with fail_lock:
            fails_by_ip.setdefault(self.client_ip(), []).append(time.time())
            fails_global.append(time.time())

    def bearer_token(self):
        auth = self.headers.get("Authorization") or ""
        if not auth.startswith("Bearer "):
            return None
        token = auth[7:].strip()
        return token if TOKEN_RE.match(token) else None

    def authorize(self):
        """Gibt (token, space) zurück oder sendet selbst eine Fehlerantwort und gibt None zurück."""
        if self.rate_limited():
            self.send_json(429, {"error": "too_many_attempts"})
            return None
        token = self.bearer_token()
        if not token:
            self.record_failure()
            self.send_json(401, {"error": "unauthorized"})
            return None
        space = find_space(token)
        if space is None and is_revoked(token):
            # Gerät wurde über „Alle anderen Geräte abmelden“ ausgesperrt
            self.send_json(410, {"error": "revoked"})
            return None
        if space is None and space_count() >= MAX_SPACES:
            # Server ist schon einem Paar zugeordnet → falsches Passwort
            self.record_failure()
            self.send_json(401, {"error": "unauthorized"})
            return None
        return token, space

    def log_message(self, fmt, *args):
        # Kurzes Log ohne Tokens oder Inhalte
        sys.stderr.write("%s %s\n" % (now_iso(), fmt % args))

    # ---------- HTTP-Methoden ----------
    def do_OPTIONS(self):
        self.send_response(204)
        self.cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path == "/v1/health":
            return self.send_json(200, {"ok": True})
        if self.path != "/v1/data":
            return self.send_json(404, {"error": "not_found"})
        auth = self.authorize()
        if not auth:
            return
        _, space = auth
        if space is None:
            return self.send_json(404, {"error": "empty"})
        return self.send_json(200, {"version": space["version"], "data": json.loads(space["data"])})

    def do_PUT(self):
        if self.path != "/v1/data":
            return self.send_json(404, {"error": "not_found"})
        auth = self.authorize()
        if not auth:
            return
        token, space = auth
        body = self.read_json()
        if not isinstance(body, dict) or not isinstance(body.get("version"), int) or not valid_envelope(body.get("data")):
            return self.send_json(400, {"error": "bad_request"})
        data_text = json.dumps(body["data"], separators=(",", ":"))
        with db_lock:
            if space is None:
                if body["version"] != 0:
                    return self.send_json(409, {"error": "conflict", "version": 0})
                count = DB.execute("SELECT COUNT(*) FROM spaces").fetchone()[0]
                if count >= MAX_SPACES:
                    return self.send_json(401, {"error": "unauthorized"})
                DB.execute(
                    "INSERT INTO spaces (token_hash, version, data, created_at, updated_at) VALUES (?, 1, ?, ?, ?)",
                    (token_hash(token), data_text, now_iso(), now_iso()),
                )
                DB.commit()
                return self.send_json(200, {"version": 1})
            current = DB.execute("SELECT version FROM spaces WHERE id = ?", (space["id"],)).fetchone()[0]
            if current != body["version"]:
                return self.send_json(409, {"error": "conflict", "version": current})
            DB.execute(
                "UPDATE spaces SET version = ?, data = ?, updated_at = ? WHERE id = ?",
                (current + 1, data_text, now_iso(), space["id"]),
            )
            DB.commit()
            return self.send_json(200, {"version": current + 1})

    def do_POST(self):
        if self.path != "/v1/rekey":
            return self.send_json(404, {"error": "not_found"})
        auth = self.authorize()
        if not auth:
            return
        _, space = auth
        if space is None:
            return self.send_json(404, {"error": "empty"})
        body = self.read_json()
        if (not isinstance(body, dict) or not isinstance(body.get("version"), int)
                or not isinstance(body.get("newToken"), str) or not TOKEN_RE.match(body["newToken"])
                or not valid_envelope(body.get("data"))):
            return self.send_json(400, {"error": "bad_request"})
        new_hash = token_hash(body["newToken"])
        revoke_old = body.get("revokeOld") is True
        with db_lock:
            if DB.execute("SELECT 1 FROM revoked WHERE token_hash = ?", (new_hash,)).fetchone():
                return self.send_json(400, {"error": "password_reused"})
            current = DB.execute("SELECT version FROM spaces WHERE id = ?", (space["id"],)).fetchone()[0]
            if current != body["version"]:
                return self.send_json(409, {"error": "conflict", "version": current})
            clash = DB.execute("SELECT id FROM spaces WHERE token_hash = ? AND id != ?", (new_hash, space["id"])).fetchone()
            if clash:
                return self.send_json(400, {"error": "bad_request"})
            old_hash = DB.execute("SELECT token_hash FROM spaces WHERE id = ?", (space["id"],)).fetchone()[0]
            DB.execute(
                "UPDATE spaces SET token_hash = ?, version = ?, data = ?, updated_at = ? WHERE id = ?",
                (new_hash, current + 1, json.dumps(body["data"], separators=(",", ":")), now_iso(), space["id"]),
            )
            if revoke_old:
                DB.execute("INSERT OR REPLACE INTO revoked (token_hash, revoked_at) VALUES (?, ?)", (old_hash, now_iso()))
            DB.commit()
            return self.send_json(200, {"version": current + 1})


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    sys.stderr.write("%s Our Mood Sync läuft auf Port %d (erlaubte Herkunft: %s)\n" % (now_iso(), PORT, ", ".join(ALLOWED_ORIGINS)))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
