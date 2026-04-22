#!/usr/bin/env python3
import http.server, socketserver, os, ssl

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(DIR, 'cert.pem')
KEY  = os.path.join(DIR, 'key.pem')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    def log_message(self, fmt, *args):
        pass

socketserver.TCPServer.allow_reuse_address = True
print(f"Gym Mobile  →  https://192.168.68.72:{PORT}")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
