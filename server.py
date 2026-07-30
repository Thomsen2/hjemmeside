import http.server
import json
import smtplib
import sys
import os
from email.message import EmailMessage
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5500
GMAIL_USER = "Thomsen2@gmail.com"
SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)

def load_env():
    env_path = SCRIPT_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_env()
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "")

def send_email(subject, body):
    if not GMAIL_APP_PASSWORD:
        print("[ERROR] GMAIL_APP_PASSWORD ikke sat i .env")
        return False, "GMAIL_APP_PASSWORD mangler"
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
        return True, None
    except Exception as e:
        print(f"[ERROR] {e}")
        return False, str(e)

def format_order(data):
    lines = [
        f"Produkt: {data.get('produkt', '')}",
        f"Besked: {data.get('besked', '')}",
        f"Afhentning: {'Ja (Dragør)' if data.get('pickup') else 'Nej'}",
        f"Forsendelse: {'Ja (55 kr)' if data.get('shipping') else 'Nej'}",
        f"Monteringskit: {'Ja (+20 kr)' if data.get('mounting') else 'Nej'}",
    ]
    if data.get("pickup"):
        lines.append(f"Afhentnings-email: {data.get('pickupEmail', '')}")
    if data.get("shipping"):
        lines.extend([
            f"Navn: {data.get('navn', '')}",
            f"Adresse: {data.get('adresse', '')}",
            f"Mail: {data.get('mail', '')}",
            f"Mobil: {data.get('mobil', '')}",
        ])
    return "\n".join(lines)

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path not in ("/send", "/api/order"):
            self.send_response(404)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"success":false,"error":"Not found"}')
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"success":false,"error":"Ugyldig JSON"}')
            return

        produkt = data.get("produkt") or data.get("product") or "Ny forespørgsel"
        body = data.get("body") or format_order(data)
        sent, err = send_email(f"Ny forespørgsel: {produkt}", body)
        payload = {"success": sent, "error": err}
        self.send_response(200 if sent else 500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

print(f"Starting server on http://127.0.0.1:{PORT}")
httpd = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
httpd.serve_forever()
