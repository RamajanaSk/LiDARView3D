
import numpy as np
import open3d as o3d


class LidarVisualizer:
    def __init__(self, points, colors):
        self.vis = o3d.visualization.Visualizer()

        success = self.vis.create_window(
            window_name="LiDARView3D - Point Cloud",
            width=1100,
            height=750,
            visible=True
        )

        if not success:
            raise RuntimeError(
                "Open3D window could not be initialized."
            )

        self.cloud = o3d.geometry.PointCloud()

        self.cloud.points = o3d.utility.Vector3dVector(points)
        self.cloud.colors = o3d.utility.Vector3dVector(colors)

        self.vis.add_geometry(self.cloud)

        options = self.vis.get_render_option()
        options.background_color = np.array([0.04, 0.05, 0.08])
        options.point_size = 2.0

        self.vis.poll_events()
        self.vis.update_renderer()

    def update(self, points, colors):
        self.cloud.points = o3d.utility.Vector3dVector(points)
        self.cloud.colors = o3d.utility.Vector3dVector(colors)

        self.vis.update_geometry(self.cloud)
        self.vis.poll_events()
        self.vis.update_renderer()

    def close(self):
        self.vis.destroy_window()
