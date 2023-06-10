from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableView, QWidget, QFileDialog, QHeaderView, QLineEdit, QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QMessageBox, QPushButton, QHBoxLayout
import csv
from password_delegate import PasswordDelegate
from aes import encrypt_password, decrypt_password, transfer_string_to_length
from PyQt5.QtCore import Qt
import os
from add_password import AddPassword
from delete_and_edit_button import delete_password, edit_password

class mainpage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_view = QTableView()

        # Set search bar
        self.search_input = QLineEdit()

        # Set up table view
        self.add_password_button = QPushButton("Add Password")

        layout = QVBoxLayout()
        layout.addWidget(self.add_password_button)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table_view)

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

        self.add_password_button.clicked.connect(self.add_password)

    def browser_files(self):
        f_name = QFileDialog.getOpenFileName(self, 'Open file', r'./', 'CSV files (*.csv)')
        self.add_password_by_import(f_name[0])

    def add_password_by_import(self, file):
        if os.path.exists("passwords.csv"):
            with open('passwords.csv', 'a', newline='') as f:
                writer_object = csv.writer(f)
                
                with open(file, "r") as import_file:
                    reader_object = csv.reader(import_file)
                    next(reader_object)

                    for row in reader_object:
                        row[3] = encrypt_password(row[3], self.get_aes_key())
                        writer_object.writerow(row)
        else:
            with open('passwords.csv', 'w', newline='') as f:
                writer_object = csv.writer(f)
                writer_object.writerow(["Name", "URL", "Username", "Password", "Note"])

                with open(file, "r") as import_file:
                    reader_object = csv.reader(import_file)
                    next(reader_object)

                    for row in reader_object:
                        row[3] = encrypt_password(row[3], self.get_aes_key())
                        writer_object.writerow(row)
        self.load_passwords()

    def load_passwords(self):
        aes_key = self.get_aes_key()
        passwords = self.read_passwords_from_csv("passwords.csv")
        print(aes_key)

        # Create the table model and set column headers
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Edit", "Name", "URL", "Username", "Password", "Note"])

        # Populate the table with passwords
        for index, password in enumerate(passwords):
            password[3] = decrypt_password(eval(password[3]), aes_key)
            row = [None, None, None, None, None, None]
            for col, field in enumerate(password):
                item = QStandardItem(field)
                row[col + 1] = item  # Start from column index 2
            model.appendRow(row)

        # Set the model for the table view
        self.table_view.setModel(model)

        self.table_view.resizeColumnsToContents()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Set the delegate for the password column
        self.table_view.setItemDelegateForColumn(4, PasswordDelegate(self))

        self.table_view.resizeColumnsToContents()

        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Add buttons to each row
        for row in range(model.rowCount()):
            edit_button = QPushButton()
            edit_button.setIcon(QIcon.fromTheme("dialog-apply"))
            edit_button.setText("Edit")
            edit_button.clicked.connect(lambda checked, row=row: self.edit_password_main(row))

            delete_button = QPushButton()
            delete_button.setIcon(QIcon.fromTheme("edit-delete"))
            delete_button.setText("Delete")
            delete_button.clicked.connect(lambda checked, row=row: self.delete_password_main(row))

            # Create a layout for the buttons
            layout = QHBoxLayout()
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)

            # Create a widget to hold the buttons layout
            widget = QWidget()
            widget.setLayout(layout)

            # Set the widget as the index widget for the row
            index = model.index(row, 0)
            self.table_view.setIndexWidget(index, widget)

    def edit_password_main(self, row):
        edit_password(self, row + 1)
        self.load_passwords()
    
    def delete_password_main(self, row):
        delete_password(self, row + 1)
        self.load_passwords()


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

    def add_password(self):
        dialog = AddPassword(self)
        if dialog.exec_() == QDialog.Accepted:
            name, url, username, password, note = dialog.get_password_details()

            password = encrypt_password(password, self.get_aes_key())
            self.save_password_to_csv(name, url, username, password, note)
            self.load_passwords()

    def save_password_to_csv(self, name, url, username, password, note):
        if not os.path.isfile("passwords.csv"):
            with open("passwords.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "URL", "Username", "Password", "Note"])
                writer.writerow([name, url, username, password, note])
        else:
            with open("passwords.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, url, username, password, note])

    def check_user_exist(self):
        if not os.path.isfile('./user_log.txt'):
            if os.path.isfile('./passwords.csv'):
                os.remove('./passwords.csv')
                QMessageBox.information(self, "Information", "No user found, please create a new user.")
                self.close()
            return False
        else:
            return True

    def get_aes_key(self):
        if self.check_user_exist():
            with open('user_log.txt', "r") as file:
                lines = file.readlines()
                password_line = lines[1].strip() 
                return transfer_string_to_length(password_line.split(",")[1].strip(), 16)
        else:
            print("aes key not found")
            self.close()
