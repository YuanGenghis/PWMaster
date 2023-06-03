import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import check_db as db_check

class SignupPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.signup_username_label = QLabel("Username:", self)
        self.signup_username_input = QLineEdit(self)

        self.signup_password_label = QLabel("Password:", self)
        self.signup_password_input = QLineEdit(self)
        self.signup_password_input.setEchoMode(QLineEdit.Password)

        self.signup_email_label = QLabel("Email:", self)
        self.signup_email_input = QLineEdit(self)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.signup)

        layout = QVBoxLayout()
        layout.addWidget(self.signup_username_label)
        layout.addWidget(self.signup_username_input)
        layout.addWidget(self.signup_password_label)
        layout.addWidget(self.signup_password_input)
        layout.addWidget(self.signup_email_label)
        layout.addWidget(self.signup_email_input)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

    def signup(self):
        username = self.signup_username_input.text()
        password = self.signup_password_input.text()
        email = self.signup_email_input.text()

        if not username or not password or not email:
            QMessageBox.warning(self, "Sign Up", "Please fill in all the fields.")
            return

        if db_check.check_user_exist(username, email):
            return
        else:
            db_check.save_user(username, password, email)

        QMessageBox.information(self, "Sign Up", "Sign up successful!")
        self.clearFields()

    def clearFields(self):
        self.signup_username_input.clear()
        self.signup_password_input.clear()
        self.signup_email_input.clear()