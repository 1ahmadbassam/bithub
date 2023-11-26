import base64
import hashlib
import pickle
import os

SECURITY_DIRECTIVE = "security_files/"
BLOCKING_HTML = SECURITY_DIRECTIVE + "blocked.html"
SECURITY_FILE = SECURITY_DIRECTIVE + "users.dat"
users = set()

BLOCKED_IP_ADDRESSES = {"172.20.10.3"}
BLOCKED_HOSTNAMES = {"steptail.com", "www.google.com", "www.microsoft.com"}

SECURED_WEBSITES = {"frogfind.com"}


def load_blocking_html():
    with open(BLOCKING_HTML, "rb") as file:
        return file.read()


def hash_credentials(credentials: bytes) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(credentials)
    return hash_object.hexdigest()


def add_new_user(credentials: bytes):
    users.add(hash_credentials(credentials))


def authenticate(credentials: bytes):
    if not users:
        load_hashed_credentials()
    if hash_credentials(credentials) in users:
        return True
    return False


def save_hashed_credentials():
    os.makedirs(SECURITY_DIRECTIVE, exist_ok=True)
    with open(SECURITY_FILE, "wb") as file:
        file.write(pickle.dumps(users))
    print("[INFO] Saved credentials for the website.")


def load_hashed_credentials():
    global users
    if os.path.exists(SECURITY_FILE):
        with open(SECURITY_FILE, "rb") as file:
            users = pickle.loads(file.read())


if __name__ == "__main__":
    user = input("Enter username: ")
    password = input("Enter password: ")
    encoded_string = base64.b64encode(f"{user}:{password}".encode())
    load_hashed_credentials()
    add_new_user(encoded_string)
    save_hashed_credentials()
