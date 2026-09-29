#!/usr/bin/env python3
"""Local-only web server for Rakshak Edge."""

from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from engine.analyzer import analyze

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
HOST = os.getenv("RAKSHAK_HOST", "127.0.0.1")
PORT = int(os.getenv("RAKSHAK_PORT", "8765"))


class Handler(BaseHTTPRequestHandler):
    server_version = "RakshakEdge/1.0"

    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data:; connect-src 'self'")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/analyze":
            self._json({"error": "Not found"}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 100_000:
                raise ValueError("Input is too large")
            data = json.loads(self.rfile.read(length) or b"{}")
            text = str(data.get("text", "")).strip()
            if not text:
                raise ValueError("Paste a message, link, or QR payload to analyze")
            self._json(analyze(text))
        except (ValueError, json.JSONDecodeError) as exc:
            self._json({"error": str(exc)}, 400)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/health":
            self._json({"status": "ready", "mode": "local", "network": "disabled"})
            return
        relative = "index.html" if path == "/" else path.lstrip("/")
        target = (WEB / relative).resolve()
        if WEB.resolve() not in target.parents and target != WEB.resolve():
            self.send_error(403)
            return
        if not target.is_file():
            self.send_error(404)
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[rakshak] {self.address_string()} {fmt % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Rakshak Edge is ready at http://{HOST}:{PORT}")
    print("Local-only mode: no message content leaves this computer.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Rakshak Edge")
    finally:
        server.server_close()
