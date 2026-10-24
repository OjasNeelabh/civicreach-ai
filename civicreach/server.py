"""
Embedded HTTP & REST API Server for CivicReach AI
Zero-dependency, multi-threaded server serving both the web application and legal API.
"""

import json
import os
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from .legal_engine import LegalEngine
from .i18n import SUPPORTED_LANGUAGES, MESSAGES

WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
engine = LegalEngine()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class CivicReachHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        # REST API endpoints
        if path == "/api/languages":
            self._send_json({"languages": SUPPORTED_LANGUAGES})
            return

        elif path == "/api/laws":
            query = params.get("q", [""])[0]
            lang = params.get("lang", ["en"])[0]
            results = engine.search(query, lang=lang)
            self._send_json({"query": query, "lang": lang, "results": results})
            return

        elif path == "/api/i18n":
            lang = params.get("lang", ["en"])[0]
            lang_dict = MESSAGES.get(lang, MESSAGES["en"])
            self._send_json({"lang": lang, "messages": lang_dict})
            return

        # Serve static web files
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            payload = {}

        if path == "/api/decrypt-notice":
            text = payload.get("text", "")
            lang = payload.get("lang", "en")
            result = engine.decrypt_notice(text, lang=lang)
            self._send_json(result)
            return

        elif path == "/api/nalsa-screener":
            lang = payload.get("lang", "en")
            result = engine.check_nalsa_eligibility(payload, lang=lang)
            self._send_json(result)
            return

        self._send_json({"error": "Endpoint not found"}, status=404)


def start_server(host: str = "0.0.0.0", port: int = 8000):
    server = ThreadedHTTPServer((host, port), CivicReachHandler)
    display_host = "localhost" if host == "0.0.0.0" else host
    print(f"\n=======================================================")
    print(f"🏛️  CivicReach AI (India Edition) Server Started")
    print(f"🌐  Web Interface: http://{display_host}:{port}")
    print(f"⚖️   Indian Legal Aid API: http://{display_host}:{port}/api/laws")
    print(f"📖  Supported Languages: English, हिन्दी, বাংলা, मराठी, தமிழ்")
    print(f"=======================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping CivicReach AI server...")
        server.server_close()
