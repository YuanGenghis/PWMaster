from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import csv

class mainpage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_view = QTableView()

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Load and display passwords
        self.load_passwords()

    def load_passwords(self):
        passwords = self.read_passwords_from_csv("passwords.csv")

        # Create the table model and set column headers
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name", "URL", "Username", "Password", "Note"])

        # Populate the table with passwords
        for password in passwords:
            row = [QStandardItem(field) for field in password]
            model.appendRow(row)

        # Set the model for the table view
        self.table_view.setModel(model)

    def read_passwords_from_csv(self, file_path):
        passwords = []

        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                passwords.append(row)

        return passwords