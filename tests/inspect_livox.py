
from pathlib import Path

data_dir = Path("data/raw")

files = list(data_dir.glob("*.LivoxDebugPointCloudData"))

if not files:
    print("No Livox files found.")
else:
    file_path = files[0]

    print("File:", file_path.name)
    print("Size:", file_path.stat().st_size, "bytes")

    with open(file_path, "rb") as file:
        header = file.read(128)

    print("First 128 bytes:")
    print(header.hex(" "))
