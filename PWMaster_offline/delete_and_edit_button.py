import csv
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import os
from aes import transfer_string_to_length, encrypt_password

def check_user_exist():
    if not os.path.isfile('./user_log.txt'):
        if os.path.isfile('./passwords.csv'):
            os.remove('./passwords.csv')
            QMessageBox.information("Information", "No user found, please create a new user.")
        return False
    else:
        return True

def edit_password(self, index):
    # Get the row data from the model
    model = self.table_view.model()
    row_data = [model.index(index - 1, column).data() for column in range(1, model.columnCount())]

    # Create the edit dialog and populate it with the row data
    dialog = EditPasswordDialog(*row_data)
    if dialog.exec_() == QDialog.Accepted:
        # Get the updated password details from the dialog
        name, url, username, password, note = dialog.get_password_details()

        # Update the CSV file with the modified password details
        update_password_in_csv(index, name, url, username, password, note)

def delete_password(self, index):
    # Confirm the deletion with a message box
    confirmation = QMessageBox.question(
        self,
        "Confirm Deletion",
        "Are you sure you want to delete this password?",
        QMessageBox.Yes | QMessageBox.No
    )

    if confirmation == QMessageBox.Yes:
        # Remove the row from the model
        model = self.table_view.model()
        model.removeRow(index)

        # Remove the corresponding password from the CSV file
        remove_password_from_csv(index)

def update_password_in_csv(row, name, url, username, password, note):
    if check_user_exist():
        with open('user_log.txt', "r") as file:
            lines = file.readlines()
            password_line = lines[1].strip() 
            user_password = password_line.split(",")[1].strip()
    else:
        user_password = "123456"
        
    with open("passwords.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    aes_key = transfer_string_to_length(user_password, 16)
    password = encrypt_password(password, aes_key)

    rows[row] = [name, url, username, password, note]

    with open("passwords.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def remove_password_from_csv(row):
    with open("passwords.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    del rows[row]

    with open("passwords.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


class EditPasswordDialog(QDialog):
    def __init__(self, name, url, username, password, note):
        super().__init__()
        self.name_input = QLineEdit()
        self.url_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.note_input = QLineEdit()

        self.name_input.setText(name)
        self.url_input.setText(url)
        self.username_input.setText(username)
        self.password_input.setText(password)
        self.note_input.setText(note)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(self.url_input)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Note:"))
        layout.addWidget(self.note_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)

        layout.addWidget(save_button)

        self.setLayout(layout)

    def get_password_details(self):
        name = self.name_input.text()
        url = self.url_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        note = self.note_input.text()

        return name, url, username, password, note