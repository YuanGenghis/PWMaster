from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QStackedWidget, QMainWindow
from signup import SignupPage
import os
from hash512 import hash_SHA512
from mainpage import mainpage

class login(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.login_username_label = QLabel("Username:", self)
        self.login_username_input = QLineEdit(self)

        self.login_password_label = QLabel("Password:", self)
        self.login_password_input = QLineEdit(self)
        self.login_password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.showSignupSection)

        self.stacked_widget = QStackedWidget(self)

        self.login_page = QWidget()
        login_layout = QVBoxLayout()
        login_layout.addWidget(self.login_username_label)
        login_layout.addWidget(self.login_username_input)
        login_layout.addWidget(self.login_password_label)
        login_layout.addWidget(self.login_password_input)
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.signup_button)
        self.login_page.setLayout(login_layout)

        self.signup_page = SignupPage()
        self.signup_page.signup_button.clicked.connect(self.signup)

        self.main_page = mainpage()

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)
        self.stacked_widget.addWidget(self.main_page)

        self.setCentralWidget(self.stacked_widget)

        
    def login(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()
        password = hash_SHA512(password)
        # Login functionality
        if os.path.exists("user_log.txt"):
            with open("user_log.txt", "r") as f:
                for i, line in enumerate(f):
                    if i == 0:
                        continue
                    elif username in line and password in line:
                        QMessageBox.information(self, "Login", "Login successful!")
                        self.showMainPage()
                        return
                QMessageBox.warning(self, "Login", "Username or password is incorrect.")

    def showSignupSection(self):
        self.stacked_widget.setCurrentWidget(self.signup_page)

    def showMainPage(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def signup(self):
        # Signup functionality
        # ...
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.signup_page