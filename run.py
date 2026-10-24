#!/usr/bin/env python3
"""
Zero-Dependency Launcher for CivicReach AI (India Edition)
Starts the local server and launches the accessible web UI.
"""

import sys
import webbrowser
import threading
import time
from civicreach.server import start_server

def open_browser(port: int):
    time.sleep(1.2)
    url = f"http://localhost:{port}"
    print(f"Opening browser at {url}...")
    try:
        webbrowser.open(url)
    except Exception:
        pass

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    # Open browser in a background thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    # Start multi-threaded server
    start_server(host="0.0.0.0", port=port)
