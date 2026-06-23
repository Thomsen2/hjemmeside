import http.server
import json
import smtplib
import sys
import os
from email.message import EmailMessage

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
GMAIL_USER = "Thomsen2@gmail.com"
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

HTML = """<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ordre bekræftet</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif;background:#f7f5f2;display:flex;justify-content:center;align-items:center;min-height:100vh}
.card{background:#fff;border-radius:16px;padding:2.5rem;max-width:420px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,0.08)}
h1{font-size:1.5rem;color:#1a1a2e;margin-bottom:0.75rem}
p{color:#555;font-size:0.95rem;line-height:1.6}
a{color:#1a1a2e}
</style>
</head>
<body>
<div class="card">
<h1>Tak for din forespørgsel</h1>
<p>Vi har modtaget din besked og vender tilbage hurtigst muligt.</p>
<p style="margin-top:1rem"><a href="/">Tilbage til forsiden</a></p>
</div>
</body>
</html>"""

def send_email(subject, body):
    if not GMAIL_APP_PASSWORD:
        print("[ERROR] GMAIL_APP_PASSWORD ikke sat")
        return False
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER
        msg.set_content(body)
        with smtplib.SMTP("smtp.gmail.com", 587) as srv:
            srv.starttls()
            srv.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            srv.send_message(msg)
        print("[OK] Email sendt")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/order":
            try:
                length = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(length))
            except:
                self.send_response(400)
                self.end_headers()
                return
            subject = data.get("product", "Ny forespørgsel")
            body = data.get("body", "")
            sent = send_email(subject, body)
            self.send_response(200 if sent else 500)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

print(f"Starting server on http://localhost:{PORT}")
httpd = http.server.HTTPServer(("localhost", PORT), Handler)
httpd.serve_forever()
