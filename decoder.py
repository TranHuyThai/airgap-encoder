from PIL import Image
import zlib

def decode_image(path, block_size=10):
    """
    Decode a single frame image into the original file bytes.
    path: path to PNG capture of your encoded grid
    block_size: same as used in encoder
    """
    img = Image.open(path).convert("L")  # grayscale
    pixels = img.load()
    
    side = img.width // block_size
    bits = ""
    
    # Rebuild bit string
    for row in range(side):
        for col in range(side):
            x = col * block_size + block_size // 2
            y = row * block_size + block_size // 2
            bits += '1' if pixels[x, y] < 128 else '0'
    
    # Convert bits → bytes
    bytes_out = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        bytes_out.append(int(byte, 2))
    
    # Parse payload
    if bytes_out[:4] != b"B2D1":
        raise ValueError("Invalid magic header, not a B2D1 file")
    
    size = int.from_bytes(bytes_out[4:8], 'big')
    data = bytes_out[8:8+size]
    crc_stored = int.from_bytes(bytes_out[8+size:12+size], 'big')
    
    # Verify CRC
    crc_calc = zlib.crc32(data)
    if crc_calc != crc_stored:
        raise ValueError("CRC mismatch, file corrupted")
    
    return data


if __name__ == "__main__":
    output_bytes = decode_image("/workspaces/airgap-encoder/frame (2).png", block_size=10)
    with open("decoded_file", "wb") as f:
        f.write(output_bytes)
    
    print("File decoded successfully!")
