# before you run this code, you have to run the command "pip install customtkinter" on your terminal

import customtkinter as ctk
import tkinter as tk
import hashlib
import caching
import os
import pickle
import sys
import threading
from server import run_server


ctk.set_appearance_mode("Dark")


ADMINISTRATOR_DIRECTIVE = "administrator_files/"
ADMINISTRARTOR_FILE = ADMINISTRATOR_DIRECTIVE + "users.dat"

users = {}


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
    with open(ADMINISTRARTOR_FILE, "wb") as file:
        file.write(pickle.dumps(users))
    print("[INFO] Saved administrator credentials.")


def load_hashed_credentials():
    global users
    if os.path.exists(ADMINISTRARTOR_FILE):
        with open(ADMINISTRARTOR_FILE, "rb") as file:
            users = pickle.loads(file.read())


def create_new_account(username: str, password: str) -> bool:
    global registration_window
    if not username or not password:
        print("[Warning] Empty username or password.")
        return False
    elif username in users:
        print("[Warning] Username already exists, try a different username.")
    else:
        users[username] = hash_credentials(password)
        print(users)
        registration_window.destroy()
        root.deiconify()
        return True


def authenticate(username: str, password: str) -> None:
    if username not in users:
        print("[Warning] Username does not exist.")
    elif users[username] == hash_credentials(password):
        open_proxy()
    else:
        print("[Warning] Password doesn't match username")


def go_back():
    registration_window.destroy()
    root.deiconify()


def exit_script():
    print("[INFO] Server is terminating...")
    caching.save_globals()
    save_hashed_credentials()
    exit(0)


def open_proxy():
    global root
    root.iconify()  # Close the old window
    new_window = ctk.CTkToplevel()  # Create a new window
    new_window.geometry("800x500")
    new_window.title("proxy")

    # Create a frame inside the new window
    frame = ctk.CTkFrame(master=new_window,fg_color="#821D1A")
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="Bithub")
    label.pack(pady=15, padx=10)

    # Create a text area widget to display console output
    text_area = ctk.CTkTextbox(master=frame)
    text_area.pack(padx=10, pady=10, fill="both", expand=True)

    # Redirect console output to the text area
    sys.stdout = ConsoleRedirector(text_area)

    run_server_thread = threading.Thread(target=run_server)
    run_server_thread.daemon = True
    run_server_thread.start()

    exit_button = ctk.CTkButton(master=frame, text="Exit", command=lambda: exit_script(), fg_color=("black"), hover_color=("black"), hover=True)
    exit_button.pack(pady=12, padx=12)


def open_registration_window():
    global registration_window, root, users
    root.iconify()  # Close the old window
    registration_window = ctk.CTkToplevel()  # Create a new window
    registration_window.title("proxy")
    registration_window.geometry("800x500")
    registration_window.title("Registration")

    # Create a frame inside the new window
    frame = ctk.CTkFrame(master=registration_window)
    frame.pack(pady=100, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(
        master=frame, text="Create a new account", font=("Roboto", 20))
    label.pack(pady=25, padx=10)

    username = ctk.CTkEntry(master=frame, placeholder_text="Username")
    username.pack(pady=5, padx=12)

    password = ctk.CTkEntry(
        master=frame, placeholder_text="Password", show="*")
    password.pack(pady=12, padx=12)

    button = ctk.CTkButton(master=frame, text="Create account", command=lambda: create_new_account(
        username.get(), password.get()), fg_color=("#DB3E39", "#821D1A"), hover_color=("#DB3E39", "#821D1A"), hover=True)
    button.pack(pady=12, padx=12)

    label2 = ctk.CTkLabel(master=frame, text="Already have an account, sign in here", font=(
        "Roboto", 10), cursor="hand2", text_color=("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)

    # Bind the click event to go back to the sign-in page
    label2.bind("<Button-1>", lambda event: go_back())


def open_sign_in():
    global root
    load_hashed_credentials()
    root = ctk.CTk()
    root.geometry("1000*1000")
    root.title("login")

    ctk.set_widget_scaling(1.5)
    ctk.set_window_scaling(1.5)

    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=100, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(
        master=frame, text="Login System", font=("Roboto", 24))
    label.pack(pady=30, padx=10)

    username = ctk.CTkEntry(master=frame, placeholder_text="Username")
    username.pack(pady=0, padx=12)

    password = ctk.CTkEntry(
        master=frame, placeholder_text="Password", show="*")
    password.pack(pady=12, padx=12)

    button = ctk.CTkButton(master=frame, text="Login", command=lambda: authenticate(username.get(
    ), password.get()), fg_color=("#DB3E39", "#821D1A"), hover_color=("#DB3E39", "#821D1A"), hover=True)
    button.pack(pady=12, padx=12)

    checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12, padx=12)

    label2 = ctk.CTkLabel(master=frame, text="Don't have an account, create a new one here", font=(
        "Roboto", 10), cursor="hand2", text_color=("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)
    # Bind the click event to open the registration window
    label2.bind("<Button-1>", lambda event: open_registration_window())

    root.mainloop()


if __name__ == "__main__":
    open_sign_in()
