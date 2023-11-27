# before you run this code, you have to run the command "pip install customtkinter" on your terminal

import hashlib
import os
import pickle
import sys
import threading
import customtkinter as ctk
import caching
from server import run_server

ctk.set_appearance_mode("Dark")

ADMINISTRATOR_DIRECTIVE = "administrator_files/"
ADMINISTRATOR_FILE = ADMINISTRATOR_DIRECTIVE + "users.dat"

users = {}

# create a class that redirects the console output to the text area frame
class ConsoleRedirector:
    def __init__(self, text_area):
        self.text_area = text_area

    def write(self, message):
        self.text_area.insert("end", message)
        self.text_area.see("end")


def hash_credentials(credentials):
    hash_object = hashlib.sha256()
    hash_object.update(credentials.encode())
    return hash_object.hexdigest()


def save_hashed_credentials():
    os.makedirs(ADMINISTRATOR_DIRECTIVE, exist_ok=True)
    with open(ADMINISTRATOR_FILE, "wb") as file:
        file.write(pickle.dumps(users))
    print("[INFO] Saved administrator credentials.")


def load_hashed_credentials():
    global users
    if os.path.exists(ADMINISTRATOR_FILE):
        with open(ADMINISTRATOR_FILE, "rb") as file:
            users = pickle.loads(file.read())

# a function that creates a new account
def create_new_account(username: str, password: str) -> bool:
    global registration_window
    # check if username and password fields are empty
    if not username or not password:
        print("[Warning] Empty username or password.")
        return False
    # check if username already exists
    elif username in users:
        print("[Warning] Username already exists, try a different username.")
    # save username and password to users
    else:
        users[username] = hash_credentials(password)
        print(users)
        registration_window.destroy()
        open_sign_in()
        return True


# a function that checks that the username and password exist and match in the users dictionary
def authenticate(username: str, password: str) -> None:
    global proxy_window
    if username not in users:
        print("[Warning] Username does not exist.")
    elif users[username] == hash_credentials(password):
        sign_in_window.destroy()
        proxy_window.deiconify()
        # start the server once authentication is succesfull
        run_server_thread = threading.Thread(target=run_server)
        run_server_thread.daemon = True
        run_server_thread.start()
    else:
        print("[Warning] Password doesn't match username.")


# a function that closes the registration window and opens the sign in window
def go_back_to_sign_in():
    registration_window.destroy()
    open_sign_in()


# a function that closes the proxy and saves the global variables
def exit_script():
    print("[INFO] Server is terminating...")
    caching.save_globals()
    save_hashed_credentials()
    exit(0)

# open the proxy window
def open_proxy():
    global sign_in_window, proxy_window

    # create the proxy window
    proxy_window = ctk.CTk()  
    proxy_window.geometry("800x500")
    proxy_window.title("proxy")
    proxy_window.iconify()
    open_sign_in() 

    # create a frame inside the new window
    frame = ctk.CTkFrame(master=proxy_window, fg_color="#821D1A")
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    title = ctk.CTkLabel(master=frame, text="BITHUB")
    title.pack(pady=15, padx=10)

    # create a text area widget to display console output
    terminal_frame = ctk.CTkTextbox(master=frame)
    terminal_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # redirect console output to the text area
    sys.stdout = ConsoleRedirector(terminal_frame)

    # exit button that closes the server
    exit_button = ctk.CTkButton(master=frame, text="Exit", command=lambda: exit_script(), fg_color="black", hover_color="black", hover=True)
    exit_button.pack(pady=12, padx=12)
    proxy_window.mainloop()


def open_registration_window():
    global registration_window, sign_in_window, users
    
    # close the old window
    sign_in_window.destroy()  

    # create the sign up window
    registration_window = ctk.CTkToplevel()  
    registration_window.title("proxy")
    registration_window.geometry("800x500")
    registration_window.title("Registration")

    # create a frame inside the new window
    frame = ctk.CTkFrame(master=registration_window)
    frame.pack(pady=100, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="Create a new account", font=("Roboto", 20))
    label.pack(pady=25, padx=10)

    # create fields for username and password
    username_for_registration = ctk.CTkEntry(master=frame, placeholder_text="Username")
    username_for_registration.pack(pady=5, padx=12)

    password_for_registration = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_for_registration.pack(pady=12, padx=12)

    # create a button that creates an account and redirects you to the sign in page
    create_account_button = ctk.CTkButton(master=frame, text="Create account", command=lambda: create_new_account(username_for_registration.get(), password_for_registration.get()), fg_color=("#DB3E39", "#821D1A"), hover_color=("#DB3E39", "#821D1A"), hover=True)
    create_account_button.pack(pady=12, padx=12)

    label2 = ctk.CTkLabel(master=frame, text="Already have an account, sign in here", font=("Roboto", 10), cursor="hand2", text_color=("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)

    # bind the click event to go back to the sign-in page
    label2.bind("<Button-1>", lambda event: go_back_to_sign_in())


def open_sign_in():
    global sign_in_window

    load_hashed_credentials()

    # create the sign in window
    sign_in_window = ctk.CTkToplevel()
    sign_in_window.geometry("800x500")
    sign_in_window.title("login")

    ctk.set_widget_scaling(1.5)
    ctk.set_window_scaling(1.5)

    frame = ctk.CTkFrame(master=sign_in_window)
    frame.pack(pady=100, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
    label.pack(pady=30, padx=10)

    # create username and password fields
    username_for_sign_in = ctk.CTkEntry(master=frame, placeholder_text="Username")
    username_for_sign_in.pack(pady=0, padx=12)

    password_for_sign_in = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_for_sign_in.pack(pady=12, padx=12)

    # create a sign-in button that authenticates user then starts the proxy server
    sign_in_button = ctk.CTkButton(master=frame, text="Login", command=lambda: authenticate(username_for_sign_in.get(), password_for_sign_in.get()), fg_color=("#DB3E39", "#821D1A"), hover_color=("#DB3E39", "#821D1A"), hover=True)
    sign_in_button.pack(pady=12, padx=12)

    checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12, padx=12)

    label2 = ctk.CTkLabel(master=frame, text="Don't have an account, create a new one here", font=("Roboto", 10), cursor="hand2", text_color=("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)

    # bind the click event to open the registration window
    label2.bind("<Button-1>", lambda event: open_registration_window())


if __name__ == "__main__":
    open_proxy()
