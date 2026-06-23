import http.server
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
    print(f"Serving at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
