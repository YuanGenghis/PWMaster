from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableView, QWidget, QHeaderView, QLineEdit, QDialog, QDialogButtonBox, QLabel, QFormLayout

class AddPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Password")
        self.layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.url_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.note_input = QLineEdit()

        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("URL:", self.url_input)
        self.layout.addRow("Username:", self.username_input)
        self.layout.addRow("Password:", self.password_input)
        self.layout.addRow("Note:", self.note_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_password_details(self):
        name = self.name_input.text()
        url = self.url_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        note = self.note_input.text()

        return name, url, username, password, note