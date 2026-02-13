from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import zlib
import struct
import math
import os


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/grid"):
            payload = build_payload("test_file.py")
            grid = payload_to_grid(payload)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(grid).encode())

        else:
            # Serve index.html if it exists
            if os.path.exists("index2.html"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                with open("index2.html", "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")


def build_payload(filepath):
    """Building payload from filepath, more info on payload structure in README"""
    with open(filepath, "rb") as f:
        data = f.read()

    magic = b"B2D1"
    # Use Big Endian
    size = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(data))

    payload = magic + size + data + crc
    return payload


def payload_to_grid(payload):
    bits = "".join(f"{b:08b}" for b in payload)

    side = math.ceil(math.sqrt(len(bits)))

    # pad with zeros
    bits = bits.ljust(side * side, "0")

    return {"side": side, "bits": bits}


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Serving on http://localhost:8000")
    server.serve_forever()
