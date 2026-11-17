
import sys

from PySide6.QtWidgets import QApplication
from src.ui.viewer_window import ViewerWindow


def main():
    app = QApplication(sys.argv)

    window = ViewerWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
