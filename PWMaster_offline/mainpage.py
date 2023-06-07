from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableView, QWidget, QFileDialog, QHeaderView, QLineEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import csv
from password_delegate import PasswordDelegate
from aes import encrypt_password, decrypt_password, transfer_string_to_length
from PyQt5.QtCore import Qt
import os

if os.path.isfile('./user_log.txt'):
    with open('user_log.txt', "r") as file:
        lines = file.readlines()
        password_line = lines[1].strip() 
        user_password = password_line.split(",")[1].strip()
else:
    user_password = "123456"

aes_key = transfer_string_to_length(user_password, 16)

class mainpage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_view = QTableView()

        # Set search bar
        self.search_input = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(self.search_input)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction('&Import Passwords', self.browser_files)

        # Load and display passwords
        self.load_passwords()

        # Set search bar functionality
        self.search_input.textChanged.connect(self.search_passwords)

    def browser_files(self):
        f_name = QFileDialog.getOpenFileName(self, 'Open file', r'./', 'CSV files (*.csv)')
        self.add_password_by_import(f_name[0])

    def add_password_by_import(self, file):
        with open('passwords.csv', 'a', newline='') as f:
            writer_object = csv.writer(f)
            
            with open(file, "r") as import_file:
                reader_object = csv.reader(import_file)
                next(reader_object)

                for row in reader_object:
                    row[3] = encrypt_password(row[3], aes_key)
                    writer_object.writerow(row)
        self.load_passwords()

    def load_passwords(self):
        passwords = self.read_passwords_from_csv("passwords.csv")

        # Create the table model and set column headers
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name", "URL", "Username", "Password", "Note"])

        # Populate the table with passwords
        for password in passwords:
            password[3] = decrypt_password(eval(password[3]), aes_key)
            row = [QStandardItem(field) for field in password]
            model.appendRow(row)

        # Set the model for the table view
        self.table_view.setModel(model)

        self.table_view.resizeColumnsToContents()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Set the delegate for the password column
        self.table_view.setItemDelegateForColumn(3, PasswordDelegate(self))

        self.table_view.resizeColumnsToContents()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def read_passwords_from_csv(self, file_path):
        passwords = []

        if os.path.isfile(file_path):
            with open(file_path, "r", newline="") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    passwords.append(row)

        return passwords
    
    def search_passwords(self):
        search_text = self.search_input.text().strip().lower()

        model = self.table_view.model()
        num_rows = model.rowCount()

        for row in range(num_rows):
            name_index = model.index(row, 0)
            url_index = model.index(row, 1)

            name = model.data(name_index, Qt.DisplayRole).lower()
            url = model.data(url_index, Qt.DisplayRole).lower()

            if search_text in name or search_text in url:
                self.table_view.setRowHidden(row, False)
            else:
                self.table_view.setRowHidden(row, True)