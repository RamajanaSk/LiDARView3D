
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QComboBox
)

from src.frame_manager import FrameManager
from src.visualizer import LidarVisualizer


class ViewerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LiDARView3D - Playback Controls")
        self.resize(700, 180)

        self.frames = FrameManager()
        initial_points, initial_colors = self.frames.get_frame(0)

        self.viewer = LidarVisualizer(
        initial_points,
        initial_colors
        )

        self.current_frame = 0
        self.playing = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)

        self.setup_ui()
        self.show_frame(0)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.time_label = QLabel("00:00.0 / 00:20.0")
        layout.addWidget(self.time_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, self.frames.total_frames - 1)
        self.slider.valueChanged.connect(self.show_frame)
        layout.addWidget(self.slider)

        controls = QHBoxLayout()

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_play)
        controls.addWidget(self.play_button)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(lambda: self.slider.setValue(0))
        controls.addWidget(reset_button)

        self.speed = QComboBox()
        self.speed.addItems(["0.5x", "1x", "2x"])
        self.speed.setCurrentText("1x")
        self.speed.currentTextChanged.connect(self.update_speed)
        controls.addWidget(self.speed)

        layout.addLayout(controls)

    def show_frame(self, index):
        self.current_frame = index

        points, colors = self.frames.get_frame(index)
        self.viewer.update(points, colors)

        current = index / self.frames.fps
        total = self.frames.total_frames / self.frames.fps

        self.time_label.setText(
            f"{current:.1f}s / {total:.1f}s"
        )

    def next_frame(self):
        if self.current_frame >= self.frames.total_frames - 1:
            self.toggle_play()
            return

        self.slider.setValue(self.current_frame + 1)

    def toggle_play(self):
        self.playing = not self.playing

        if self.playing:
            if self.current_frame >= self.frames.total_frames - 1:
                self.slider.setValue(0)

            self.update_speed()
            self.play_button.setText("Pause")
        else:
            self.timer.stop()
            self.play_button.setText("Play")

    def update_speed(self):
        if not self.playing:
            return

        speed = float(self.speed.currentText().replace("x", ""))
        interval = round(1000 / (self.frames.fps * speed))

        self.timer.start(interval)

    def closeEvent(self, event):
        self.timer.stop()
        self.viewer.close()
        event.accept()
