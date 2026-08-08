"""
Servidor HTTP simples para servir o jogo AlienFall48 (build web pygbag).
Usado pelo Render para hospedar o jogo no browser via WebAssembly.
"""
import http.server
import socketserver
import os
import sys

PORT = int(os.environ.get("PORT", 8000))
WEB_DIR = os.path.join(os.path.dirname(__file__), "docs")

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        # Necessário para SharedArrayBuffer (pygbag requer esses headers)
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format, *args):
        pass  # silenciar logs de acesso

print(f"AlienFall48 rodando em http://0.0.0.0:{PORT}")
print(f"Servindo arquivos de: {WEB_DIR}")

with socketserver.TCPServer(("", PORT), CORSHandler) as httpd:
    httpd.allow_reuse_address = True
    httpd.serve_forever()
