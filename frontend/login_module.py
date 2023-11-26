# before you run this code, you have to run the command "pip install customtkinter" on your terminal

import customtkinter as ctk
import hashlib
from httplib import requests
from security import hash_credentials
import os
import pickle

ctk.set_appearance_mode("Light")

ADMINISTRATOR_DIRECTIVE = "administrator"
ADMINISTRARTOR_FILE = ADMINISTRATOR_DIRECTIVE + "users.dat"

users = {}

req = '''GET http://sdfox7.com/ HTTP/1.1\r\nAccept: image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, */*\r\nAccept-Language: en\r\nUA-pixels: 1024x768\r\nUA-color: color16\r\nUA-OS: Windows NT\r\nUA-CPU: x86\r\nUser-Agent: Mozilla/2.0 (compatible; MSIE 3.01; Windows NT)\r\nHost: sdfox7.com\r\nConnection: Keep-Alive\r\n\r\nGET http://sdfox7.com/xp/authcab.jpg HTTP/1.1\r\nHost: sdfox7.com\r\nConnection: keep-alive\r\n\r\nhttp://sdfox7.com/xp/ie8cert.jpg'''


def save_hashed_credentials():
    os.makedirs(ADMINISTRATOR_DIRECTIVE, exist_ok=True)
    with open(ADMINISTRARTOR_FILE, "wb") as file:
        file.write(pickle.dumps(users))
    print("[INFO] Saved credentials for the website.")


def load_hashed_credentials():
    global users
    if os.path.exists(ADMINISTRARTOR_FILE):
        with open(ADMINISTRARTOR_FILE, "rb") as file:
            users = pickle.loads(file.read())


def create_new_account(username: str, password: str) -> bool:
    global registration_window
    if not username or not password:
        print("empty username or password.")
        return False
    elif username in users:
        print("Username already exists, try a different username.")
    else:
        users[username] = hash_credentials(password)
        print(users)
        registration_window.destroy()
        root.deiconify()
        return True


def Print(printable: str):
    tabview = ctk.CTkTabview(master=frame)
    tabview.pack(padx=20, pady=0)
    label2 = ctk.CTkLabel(master=tabview.tab("tab 1"), text=str(requests.parse(printable)), font=("Roboto", 10), cursor="hand2",
                          text_color=("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)


def authenticate(username: str, password: str) -> None:
    if not username:
        open_proxy()
    elif username not in users:
        print("username doesn't exist.")
    else:
        if users[username] == hash_credentials(password):
            open_proxy()
        else:
            print("password doesn't match username")


def goBack():
    registration_window.destroy()
    root.deiconify()


def open_proxy():
    global root
    root.iconify()  # Close the old window
    new_window = ctk.CTkToplevel()  # Create a new window
    new_window.geometry("800x500")
    new_window.title("proxy")

    # Create a frame inside the new window
    frame = ctk.CTkFrame(master=new_window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    label = ctk.CTkLabel(master=frame, text="Proxy Sever")
    label.pack(pady=15, padx=10)

    tabview = ctk.CTkTabview(master=frame)
    tabview.pack(padx=20, pady=0)

    tabview.add("tab 1")
    tabview.add("tab 2")
    tabview.add("tab 3")
    tabview.add("tab 4")
    tabview.add("tab 5")
    tabview.set("tab 1")

    label2 = ctk.CTkLabel(master=tabview.tab("tab 1"), text=str(requests.parse(req)), font=("Roboto", 10), cursor="hand2",
                          text_color=("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)


def open_registration_window():
    global registration_window, root, users
    load_hashed_credentials()
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

    button = ctk.CTkButton(master=frame, text="Create account",
                           command=lambda: create_new_account(
                               username.get(), password.get()),
                           fg_color=("#DB3E39", "#821D1A"), hover_color=("#DB3E39", "#821D1A"), hover=True)
    button.pack(pady=12, padx=12)

    label2 = ctk.CTkLabel(master=frame, text="Already have an account, sign in here", font=("Roboto", 10),
                          cursor="hand2", text_color=("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)
    # Bind the click event to go back to the sign-in page
    label2.bind("<Button-1>", lambda event: goBack())


def open_sign_in():
    global root
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

    button = ctk.CTkButton(master=frame, text="Login", command=lambda: authenticate(username.get(), password.get()),
                           fg_color=("#DB3E39", "#821D1A"), hover_color=("#DB3E39", "#821D1A"), hover=True)
    button.pack(pady=12, padx=12)

    checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12, padx=12)

    label2 = ctk.CTkLabel(master=frame, text="Don't have an account, create a new one here", font=("Roboto", 10),
                          cursor="hand2", text_color=("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)
    label2.bind("<Button-1>",
                lambda event: open_registration_window())  # Bind the click event to open the registration window

    root.mainloop()
