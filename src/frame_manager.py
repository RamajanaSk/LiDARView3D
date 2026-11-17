
import numpy as np


class FrameManager:
    def __init__(self, fps=10, duration=20):
        self.fps = fps
        self.duration = duration
        self.total_frames = fps * duration

        rng = np.random.default_rng(42)

        self.road = np.column_stack([
            rng.uniform(-20, 20, 4000),
            rng.uniform(-5, 5, 4000),
            rng.normal(0, 0.015, 4000)
        ])

        self.car = rng.uniform(
            [-1.8, -0.8, 0.2],
            [1.8, 0.8, 1.5],
            (1500, 3)
        )

        self.person = rng.uniform(
            [-0.2, -0.2, 0],
            [0.2, 0.2, 1.8],
            (400, 3)
        )

    def get_frame(self, index):
        index = max(0, min(index, self.total_frames - 1))
        t = index / self.fps

        car = self.car + np.array([
            -15 + 1.5 * t, -2.0, 0
        ])

        person = self.person + np.array([
            4.0, -4.0 + 0.4 * t, 0
        ])

        points = np.vstack([self.road, car, person])

        colors = np.vstack([
            np.tile([0.35, 0.35, 0.35], (len(self.road), 1)),
            np.tile([0.1, 0.8, 1.0], (len(car), 1)),
            np.tile([1.0, 0.6, 0.1], (len(person), 1))
        ])

        return points, colors
