import sys
import os
from hash512 import hash_SHA512
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class SignupPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.signup_username_label = QLabel("Username:", self)
        self.signup_username_input = QLineEdit(self)

        self.signup_password_label = QLabel("Password:", self)
        self.signup_password_input = QLineEdit(self)
        self.signup_password_input.setEchoMode(QLineEdit.Password)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.signup)

        layout = QVBoxLayout()
        layout.addWidget(self.signup_username_label)
        layout.addWidget(self.signup_username_input)
        layout.addWidget(self.signup_password_label)
        layout.addWidget(self.signup_password_input)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

    def signup(self):
        username = self.signup_username_input.text()
        password = self.signup_password_input.text()
        print(password)
        password = hash_SHA512(password)

        if not username or not password :
            QMessageBox.warning(self, "Sign Up", "Please fill in all the fields.")
            return
        
        if not self.check_user_log_exist():
            with open("user_log.txt", "w+") as f:
                f.write("user_name, password\n")
                f.write(username + "," + password)

        QMessageBox.information(self, "Sign Up", "Sign up successful!")
        self.clearFields()

    def clearFields(self):
        self.signup_username_input.clear()
        self.signup_password_input.clear()

    def check_user_log_exist(self):
        return os.path.exists("user_log.txt")
