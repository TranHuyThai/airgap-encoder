from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import struct
import math
import zlib
import json
from urllib.parse import urlparse, parse_qs

PORT = 8000
FOLDER = "./"
EXT = ".png"

# --- Payload functions ---
def build_payload(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    magic = b"B2D1"
    size = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(data))
    return magic + size + data + crc

def payload_to_grid(payload):
    bits = "".join(f"{b:08b}" for b in payload)
    side = math.ceil(math.sqrt(len(bits)))
    bits = bits.ljust(side * side, "0")
    return {"side": side, "bits": bits}

# --- HTTP Handler ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/files":
            py_files = []
            for root, dirs, files in os.walk(FOLDER):
                for file in files:
                    if file.endswith(EXT):
                        py_files.append(os.path.join(root, file))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(py_files).encode())

        elif parsed.path == "/grid":
            qs = parse_qs(parsed.query)
            if "file" in qs:
                file_path = qs["file"][0]
                if os.path.exists(file_path):
                    payload = build_payload(file_path)
                    grid = payload_to_grid(payload)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(grid).encode())
                    return
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request: file not found")

        elif parsed.path == "/":
            if os.path.exists("index.html"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("index.html", "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"Serving on http://localhost:{PORT}")
    server.serve_forever()
