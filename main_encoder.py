from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import struct
import math
import zlib
import json
from urllib.parse import urlparse, parse_qs

PORT = 8000
FOLDER = "./"
EXT = ".py"

# --- Payload functions ---
def build_chunk(filepath, index, chunk_size):
    with open(filepath, "rb") as f:
        data = f.read()

    total_chunks = math.ceil(len(data) / chunk_size)

    start = index * chunk_size
    end = start + chunk_size
    chunk_data = data[start:end]

    magic = b"B2D1"
    total = struct.pack(">H", total_chunks)
    idx = struct.pack(">H", index)
    length = struct.pack(">H", len(chunk_data))
    crc = struct.pack(">I", zlib.crc32(chunk_data))

    return magic + total + idx + length + chunk_data + crc

def payload_to_grid(filepath, index=0):
    SIDE = 128
    MAX_BYTES = (SIDE * SIDE) // 8
    HEADER_SIZE = 14
    DATA_SIZE = MAX_BYTES - HEADER_SIZE

    payload = build_chunk(filepath, index, DATA_SIZE)

    bits = "".join(f"{b:08b}" for b in payload)
    bits = bits.ljust(SIDE * SIDE, "0")

    with open(filepath, "rb") as f:
        total_chunks = math.ceil(len(f.read()) / DATA_SIZE)

    return {
        "side": SIDE,
        "bits": bits,
        "total": total_chunks
    }

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
                index = int(qs.get("index", [0])[0])

                if os.path.exists(file_path):
                    grid = payload_to_grid(file_path, index)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(grid).encode())
                    return

            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request")

        elif parsed.path == "/":
            if os.path.exists("encoder.html"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("encoder.html", "rb") as f:
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