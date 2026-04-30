# Login View
# Simple login dialog for authentication

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox)
from PyQt6.QtCore import Qt


class LoginDialog(QDialog):
    """Login dialog for user authentication"""
    
    # Default credentials
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "admin123"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("THPT Grade Manager - Login")
        self.setGeometry(500, 250, 400, 200)
        self.setModal(True)
        self.authenticated = False
        
        # Prevent close button from closing without login
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Đăng Nhập Hệ Thống")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Username
        username_label = QLabel("Tên đăng nhập:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tên đăng nhập")
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Mật khẩu:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhập mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        login_btn = QPushButton("Đăng Nhập")
        login_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        login_btn.clicked.connect(self.handle_login)
        
        exit_btn = QPushButton("Thoát")
        exit_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        exit_btn.clicked.connect(self.handle_exit)
        
        button_layout.addWidget(login_btn)
        button_layout.addWidget(exit_btn)
        
        layout.addSpacing(10)
        layout.addLayout(button_layout)
        
        # Demo hint
        demo_hint = QLabel("Demo: admin / admin123")
        demo_hint.setStyleSheet("color: #666; font-size: 10px; margin-top: 10px;")
        layout.addWidget(demo_hint)
        
        self.setLayout(layout)
        
        # Focus on username input
        self.username_input.setFocus()
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu!")
            return
        
        if username == self.VALID_USERNAME and password == self.VALID_PASSWORD:
            self.authenticated = True
            self.accept()
        else:
            QMessageBox.critical(self, "Lỗi Đăng Nhập", 
                               "Tên đăng nhập hoặc mật khẩu không chính xác!\n\nVui lòng thử lại.")
            self.password_input.clear()
            self.username_input.setFocus()
    
    def handle_exit(self):
        """Handle exit button click"""
        reply = QMessageBox.question(self, "Xác Nhận", 
                                    "Bạn có chắc chắn muốn thoát ứng dụng?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.reject()
    
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.handle_login()
        elif event.key() == Qt.Key.Key_Escape:
            self.handle_exit()
        else:
            super().keyPressEvent(event)
