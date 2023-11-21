# before you run this code, you have to  run the command "pip install customtkinter" on your terminal

import customtkinter
import hashlib

# need serialization and deserialization
accounts = {}


def hash_password(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    return hash_object.hexdigest()


def create_new_account(username, password):
    if username in accounts:
        return False
    else:
        accounts[username] = hash_password(password)
        return True
