from db_connect import db
from PyQt5.QtWidgets import QMessageBox

# Check if the user already exists in the database
def check_user_exist(username, email):
    cursor = db.cursor()
    name_query = "SELECT * FROM user WHERE Username = %s"
    cursor.execute(name_query, (username,))
    user_name = cursor.fetchone()
    email_query = "SELECT * FROM user WHERE Email = %s"
    cursor.execute(email_query, (email,))
    user_email = cursor.fetchone()
    cursor.close()

    if user_name:
        QMessageBox.warning("Sign Up", "Username already exists.")
        return True
    elif user_email:
        QMessageBox.warning("Sign Up", "Email already exists.")
        return True
    else:
        return False

# Save the user information to the database
def save_user(username, password, email):
    cursor = db.cursor()
    query = "INSERT INTO User (Username, Password, Email) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, email))
    db.commit()
    cursor.close()