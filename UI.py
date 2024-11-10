import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QPushButton, QLabel, QTextEdit, QMessageBox, 
                            QFrame, QSizePolicy)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class InstagramMockUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Instagram')
        self.setFixedSize(400, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial;
            }
            QLineEdit, QTextEdit {
                padding: 12px;
                border: 1px solid #dbdbdb;
                border-radius: 4px;
                font-size: 14px;
                color: #262626;
            }
            QLineEdit::placeholder, QTextEdit::placeholder {
                color: #8e8e8e;
            }
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #262626;
            }
            QLabel {
                color: #262626;
            }
            #subtitle {
                color: #8e8e8e;
                font-size: 14px;
            }
            #or_label {
                color: #8e8e8e;
                font-size: 13px;
            }
            #icon_placeholder {
                background-color: white;
                border: 1px solid #dbdbdb;
                min-height: 50px;
                max-height: 50px;
                min-width: 50px;
                max-width: 50px;
                border-radius: 10px;
            }
        """)

        self.stack = QVBoxLayout()
        self.setLayout(self.stack)

        self.login_widget = QWidget()
        self.message_widget = QWidget()

        self.create_login_screen()
        self.create_message_form()

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.message_widget)

        self.show_login_screen()

    def create_login_screen(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        self.login_widget.setLayout(layout)

        # Icon placeholder
        icon_frame = QFrame()
        icon_frame.setObjectName("icon_placeholder")
        icon_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(icon_frame)
        layout.addLayout(icon_layout)
        icon_layout.setAlignment(Qt.AlignCenter)

        layout.addSpacing(10)

        # Instagram title
        logo_label = QLabel('Instagram', self)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(logo_label)

        # Subtitle
        subtitle = QLabel('Sign in to your account', self)
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Username
        username_label = QLabel('Username', self)
        layout.addWidget(username_label)
        
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText('Enter your username')
        layout.addWidget(self.username_entry)

        layout.addSpacing(10)

        # Password
        password_label = QLabel('Password', self)
        layout.addWidget(password_label)
        
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText('Enter your password')
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        layout.addSpacing(20)

        login_button = QPushButton('Log in', self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        layout.addSpacing(15)

        or_label = QLabel('OR', self)
        or_label.setObjectName("or_label")
        or_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(or_label)

        layout.addSpacing(15)

        json_button = QPushButton('Load JSON for Login', self)
        json_button.clicked.connect(self.load_json)
        layout.addWidget(json_button)

        layout.addStretch()

    def create_message_form(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        self.message_widget.setLayout(layout)

        title = QLabel('Send Message', self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)

        layout.addSpacing(20)

        self.recipient_entry = QLineEdit(self)
        self.recipient_entry.setPlaceholderText('Recipient username')
        layout.addWidget(self.recipient_entry)

        layout.addSpacing(10)

        self.message_text = QTextEdit(self)
        self.message_text.setPlaceholderText('Type your message here')
        layout.addWidget(self.message_text)

        layout.addSpacing(20)

        send_button = QPushButton('Send Message', self)
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        layout.addSpacing(10)

        logout_button = QPushButton('Log Out', self)
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        layout.addStretch()

    def show_login_screen(self):
        self.message_widget.hide()
        self.login_widget.show()

    def show_message_form(self):
        self.login_widget.hide()
        self.message_widget.show()

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        
        if username and password:
            self.show_message_form()
        else:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')

    def load_json(self):
        json_data = json.dumps({
            "username": "demo_user",
            "password": "demo_pass"
        })
        data = json.loads(json_data)
        
        self.username_entry.setText(data["username"])
        self.password_entry.setText(data["password"])

    def send_message(self):
        recipient = self.recipient_entry.text()
        message = self.message_text.toPlainText()
        
        if recipient and message:
            QMessageBox.information(self, 'Success', f'Message sent to {recipient}')
            self.recipient_entry.clear()
            self.message_text.clear()
        else:
            QMessageBox.warning(self, 'Error', 'Please enter both recipient and message')

    def logout(self):
        self.recipient_entry.clear()
        self.message_text.clear()
        self.username_entry.clear()
        self.password_entry.clear()
        self.show_login_screen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InstagramMockUI()
    ex.show()
    sys.exit(app.exec_())