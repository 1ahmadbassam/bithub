import base64
import hashlib
import pickle
import os

SECURITY_DIRECTIVE = "security/"
BLOCKING_HTML = SECURITY_DIRECTIVE + "blocked.html"
SECURITY_FILE = SECURITY_DIRECTIVE + "users.dat"
users = set()

BLOCKED_IP_ADDRESSES = {"172.20.10.3"}
BLOCKED_HOSTNAMES = {"steptail.com", "www.google.com", "www.microsoft.com"}

SECURED_WEBSITES = {"frogfind.com"}


def load_blocking_html():
    """
        Load the blocking HTML page from disk.
    """
    with open(BLOCKING_HTML, "rb") as file: # rb = read binary
        return file.read()  # return the contents of the file


def hash_credentials(credentials: bytes) -> str:
    """
        Hash the credentials using SHA256.
    """
    hash_object = hashlib.sha256() # create a hash object
    hash_object.update(credentials) # update the hash object with the credentials
    return hash_object.hexdigest() # return the hex digest of the hash object


def add_new_user(credentials: bytes):
    """
        Add a new user to the set of users.
    """
    users.add(hash_credentials(credentials)) # add the hashed credentials to the set of users


def authenticate(credentials: bytes):
    """
        Authenticate the user by checking if the hashed credentials are in the set of users.
    """
    if not users:
        load_hashed_credentials() # load the hashed credentials from disk
    if hash_credentials(credentials) in users: # check if the hashed credentials are in the set of users
        return True
    return False


def save_hashed_credentials():
    """
        Save the hashed credentials to disk.
    """
    os.makedirs(SECURITY_DIRECTIVE, exist_ok=True) # create the security directory if it doesn't exist
    with open(SECURITY_FILE, "wb") as file: # wb = write binary
        file.write(pickle.dumps(users)) # write the hashed credentials to disk
    print("[INFO] Saved credentials file to disk.") # print a message to inform


def load_hashed_credentials():
    """
        Load the hashed credentials from disk.
    """
    global users
    if os.path.exists(SECURITY_FILE): # check if the file exists
        with open(SECURITY_FILE, "rb") as file: # rb = read binary
            users = pickle.loads(file.read()) # read the hashed credentials from disk


if __name__ == "__main__": # if the script is run directly
    user = input("Enter username: ")
    password = input("Enter password: ")
    encoded_string = base64.b64encode(f"{user}:{password}".encode())
    load_hashed_credentials()
    add_new_user(encoded_string)
    save_hashed_credentials()
