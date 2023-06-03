import sys
import time
from PyQt5.QtWidgets import QApplication, QMessageBox,  QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QStackedWidget
from login import login

class PasswordManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Manager")
        self.setGeometry(1000, 800, 1000, 500)

        self.login_page = login()
        self.setCentralWidget(self.login_page)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManagerApp()
    window.show()
    sys.exit(app.exec())
