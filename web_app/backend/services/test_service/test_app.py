
import http.server
import socketserver
import json
import os

PORT = 8001
VERSION = os.getenv('APP_VERSION', 'unknown_version')

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/version':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "This is the TEST service!",
                "version": VERSION,
                "status": "OK 2"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving test_service at port {PORT}")
    print(f"Version: {VERSION}")
    httpd.serve_forever()