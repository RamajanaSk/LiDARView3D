
from pathlib import Path

DATA_DIR = Path("data/raw")

files = list(DATA_DIR.glob("*.LivoxDebugPointCloudData"))

if not files:
    raise FileNotFoundError("No Livox debug file found.")

path = files[0]

with path.open("rb") as file:
    header = file.read(128)
    first_packet = file.read(1114)

print("File version:", header[0])
print("Device type:", header[1])
print("Data type:", header[2])

serial = header[3:19].split(b"\x00")[0]
print("Serial:", serial.decode("ascii", errors="replace"))

print("First packet length:", len(first_packet))
print("First 32 packet bytes:", first_packet[:32].hex(" "))

print("Starts with 0xA5:", first_packet.startswith(b"\xA5"))

payload_size = path.stat().st_size - 128
print("Payload size:", payload_size)
print("1114-byte packet remainder:", payload_size % 1114)
