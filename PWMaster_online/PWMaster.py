import sys
import time
from PyQt5.QtWidgets import QApplication, QMessageBox,  QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QStackedWidget
from db_connect import db
from sign_up import SignupPage

# Create a cursor to execute SQL queries
cursor = db.cursor()


class PasswordManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Manager")
        self.setGeometry(1000, 800, 1000, 500)

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

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)

        self.setCentralWidget(self.stacked_widget)

    def login(self):
        # Login functionality
        # ...

        self.showPasswordManager()

    def showSignupSection(self):
        self.stacked_widget.setCurrentWidget(self.signup_page)

    def showPasswordManager(self):
        # Password manager functionality
        # ...
        pass

    def signup(self):
        # Signup functionality
        # ...

        QMessageBox.information(self, "Sign Up", "Sign up successful!")
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.signup_page


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManagerApp()
    window.show()
    sys.exit(app.exec())
