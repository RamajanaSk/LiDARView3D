
from pathlib import Path
import numpy as np


def load_lidar(file_path):
    """Load LiDAR points from an XYZI binary file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"LiDAR file not found: {file_path}"
        )

    data = np.fromfile(path, dtype=np.float32)

    if data.size % 4 != 0:
        raise ValueError("Invalid XYZI LiDAR file")

    return data.reshape(-1, 4)[:, :3]
