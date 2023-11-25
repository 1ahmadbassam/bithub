import hashlib
import pickle
import os

BLOCKING_HTML = "blocked.html"
SECURITY_DIRECTIVE = "security"
users = set()

BLOCKED_IP_ADDRESSES = {"172.20.10.3"}
BLOCKED_HOSTNAMES = {"steptail.com", "www.google.com", "www.microsoft.com"}

SECURED_WEBSITES = {"frogfind.com"}


def load_blocking_html():
    with open(BLOCKING_HTML, "rb") as file:
        return file.read()


def hash_credentials(credentials: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(credentials.encode())
    return hash_object.hexdigest()


def add_hashed_credentials_to_users(credentials: str):
    users.add(hash_credentials(credentials))


def add_new_user(credentials: str):
    users.add(hash_credentials(credentials))


def authenticate(credentials: str):
    if hash(credentials) in users:
        return True
    return False


def save_hashed_credentials(credentials: str):
        os.makedirs(SECURITY_DIRECTIVE, exist_ok=True)
        with open(SECURITY_DIRECTIVE, "wb") as file:
            file.write(pickle.dumps(users))
        print("[INFO] Saved credentials for the website.")


def load_hashed_credentials():
    global users
    if os.path.exists(SECURITY_DIRECTIVE):
        with open(SECURITY_DIRECTIVE, "rb") as file:
            users = pickle.loads(file.read())