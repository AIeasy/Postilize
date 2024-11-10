import sys
import json
import QL
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QPushButton, QLabel, QTextEdit, QMessageBox, 
                            QFrame, QSizePolicy, QComboBox, QDialog)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Message")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.message = QLabel("Are you sure you want to send this message?")
        self.message.setWordWrap(True)
        layout.addWidget(self.message)

        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Confirm")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

class InstagramMockUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ql = QL.QL()
    def initUI(self):
        self.setWindowTitle('Instagram')
        self.setFixedSize(400, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial;
            }
            QLineEdit, QTextEdit, QComboBox {
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

        # Recipient dropdown
        recipient_label = QLabel('Recipient', self)
        layout.addWidget(recipient_label)

        self.recipient_dropdown = QComboBox(self)
        self.recipient_dropdown.setEditable(True)
        self.recipient_dropdown.setInsertPolicy(QComboBox.NoInsert)
        layout.addWidget(self.recipient_dropdown)

        layout.addSpacing(10)

        # Message text area
        message_label = QLabel('Message', self)
        layout.addWidget(message_label)

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
            login_success, error_code = self.ql.login(username, password)  # Call QL.py's main function to log in
            if login_success:
                self.show_message_form()
            else:
                QMessageBox.warning(self, 'Error', f'Login failed: {error_code}')
        else:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')

    def load_json(self):
        json_data = json.dumps({
            "username": "example_username",
            "password": "example_password",
            "recipient": "instagram_user",
            "message": "Hello, this is a test message!"
        })
        data = json.loads(json_data)
        
        self.username_entry.setText(data["username"])
        self.password_entry.setText(data["password"])
        
        # Preview the loaded data
        preview = f"Username: {data['username']}\n"
        preview += f"Recipient: {data['recipient']}\n"
        preview += f"Message: {data['message']}"
        
        reply = QMessageBox.question(self, 'Preview JSON Data', 
                                     preview, 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.login()
            self.recipient_dropdown.addItem(data["recipient"])
            self.recipient_dropdown.setCurrentText(data["recipient"])
            self.message_text.setText(data["message"])

    def send_message(self):
        recipient = self.recipient_dropdown.currentText()
        message = self.message_text.toPlainText()
        
        if recipient and message:
            dialog = ConfirmDialog(self)
            if dialog.exec_():
                QMessageBox.information(self, 'Success', f'Message sent to {recipient}')
                self.recipient_dropdown.setCurrentIndex(0)
                self.message_text.clear()
        else:
            QMessageBox.warning(self, 'Error', 'Please select a recipient and enter a message')

    def logout(self):
        self.recipient_dropdown.clear()
        self.message_text.clear()
        self.username_entry.clear()
        self.password_entry.clear()
        self.show_login_screen()
    def closeEvent(self, event):
        self.ql.close()  # Ensure the browser session is closed when UI is closed
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InstagramMockUI()
    ex.show()
    sys.exit(app.exec_())