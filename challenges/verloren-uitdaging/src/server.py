"""Kleine webserver voor de verloren uitdaging.

Start met: python3 server.py   (en open http://localhost:8000)
Onbekende pagina's geven een foutpagina met details over het verzoek.
"""
import html
from http.server import HTTPServer, SimpleHTTPRequestHandler


class Handler(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        if code != 404:
            return super().send_error(code, message, explain)
        details = {
            "Requested path": self.path,
            "Method": self.command,
            "Host": self.headers.get("Host", ""),
            "Accept header": self.headers.get("Accept", ""),
        }
        rows = "".join(f"<dt>{k}:</dt><dd>{html.escape(v)}</dd>" for k, v in details.items())
        body = (
            "<!doctype html><html><head><meta charset='utf-8'><title>404 Not Found</title></head>"
            "<body style='font-family:sans-serif;text-align:center;padding:50px'>"
            "<h1>404 Not Found</h1><p>De gevraagde pagina werd niet gevonden op deze server.</p>"
            f"<dl style='display:inline-block;text-align:left;font-family:monospace'>{rows}</dl></body></html>"
        ).encode()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("", 8000), Handler).serve_forever()
