# Auth Controller
# Simple authentication controller (placeholder)

from PyQt6.QtWidgets import QWidget


class AuthController(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Xác thực")
        self.setGeometry(200, 200, 400, 300)

    def show(self):
        super().show()
