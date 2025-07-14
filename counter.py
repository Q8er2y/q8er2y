import http.server
import json
import os
from urllib.parse import urlparse

PORT = 8000
COUNTER_FILE = "count.json"

class CounterHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/increment":
            # Load counter
            if not os.path.exists(COUNTER_FILE):
                with open(COUNTER_FILE, "w") as f:
                    json.dump({"count": 0}, f)

            with open(COUNTER_FILE, "r") as f:
                data = json.load(f)

            data["count"] += 1

            with open(COUNTER_FILE, "w") as f:
                json.dump(data, f, indent=2)

            # Redirect back to main page
            self.send_response(303)
            self.send_header("Location", "/index.html")
            self.end_headers()
        else:
            self.send_error(404, "Unsupported POST path")

    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with http.server.HTTPServer(("", PORT), CounterHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
