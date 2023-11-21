#before you run this code, you have to run the command "pip install ctk" on your terminal

import customtkinter as ctk
import hashlib

ctk.set_appearance_mode("Dark")

accounts = {} 

def hash_password(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    return hash_object.hexdigest()

def create_new_account(username, password):
    global registration_window
    if not username or not password:
        print("empty username or password.")
        return False
    elif username in accounts:
        print("Username aleady exists, try a different username.")
    else:
        accounts[username] = hash_password(password)
        print(accounts)
        registration_window.destroy()
        root.deiconify()
        return True
    
def authenticate(username, password):
    if username not in accounts:
        print("username doesn't exist.")
    else:
        if accounts[username] == hash_password(password):
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

    frame = ctk.CTkFrame(master=new_window)  # Create a frame inside the new window
    frame.pack(pady=20, padx=60, fill="both", expand=True)  
    label = ctk.CTkLabel(master=frame, text="Proxy Sever")
    label.pack(pady=15, padx=10)

    tabview = ctk.CTkTabview(master=frame)
    tabview.pack(padx=20, pady=20)

    tabview.add("tab 1")  
    tabview.add("tab 2")  
    tabview.add("tab 3")  
    tabview.add("tab 4") 
    tabview.add("tab 5")  
    tabview.set("tab 1") 

    label2 = ctk.CTkLabel(master=tabview.tab("tab 1"), text="BlaBlaBla", font=("Roboto", 10), cursor="hand2", text_color= ("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)

def open_registration_window():
    global registration_window, root
    root.iconify()  # Close the old window
    registration_window = ctk.CTkToplevel()  # Create a new window 
    registration_window.title("proxy")
    registration_window.geometry("800x500") 
    registration_window.title("Registration")

    frame = ctk.CTkFrame(master=registration_window)  # Create a frame inside the new window
    frame.pack(pady=100, padx=60, fill="both", expand=True)  

    label = ctk.CTkLabel(master=frame, text="Create a new account", font=("Roboto", 20))
    label.pack(pady=25, padx=10)

    username = ctk.CTkEntry(master=frame, placeholder_text = "Username")
    username.pack(pady=5,padx=12)

    password = ctk.CTkEntry(master=frame, placeholder_text = "Password", show="*")
    password.pack(pady=12,padx=12)

    button = ctk.CTkButton(master=frame, text="Create account",command=lambda: create_new_account(username.get(), password.get()),fg_color=("#DB3E39", "#821D1A"),hover_color=("#DB3E39", "#821D1A"),hover=True)
    button.pack(pady=12,padx=12)

    label2 = ctk.CTkLabel(master=frame, text="Already have an account, sign in here", font=("Roboto", 10), cursor="hand2", text_color= ("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)
    label2.bind("<Button-1>", lambda event: goBack())  # Bind the click event to go back to the sign in page

def open_sign_in():
    global root
    root = ctk.CTk()
    root.geometry("1000*1000")
    root.title("login")

    ctk.set_widget_scaling(1.5)  
    ctk.set_window_scaling(1.5)  

    frame = ctk.CTkFrame(master = root)
    frame.pack(pady=100, padx=60,fill="both",expand=True)

    label = ctk.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
    label.pack(pady=30,padx=10)

    username = ctk.CTkEntry(master=frame, placeholder_text = "Username")
    username.pack(pady=0,padx=12)

    password = ctk.CTkEntry(master=frame, placeholder_text = "Password", show="*")
    password.pack(pady=12,padx=12)

    button = ctk.CTkButton(master=frame, text="Login",command=lambda: authenticate(username.get(), password.get()),fg_color=("#DB3E39", "#821D1A"),hover_color=("#DB3E39", "#821D1A"),hover=True)
    button.pack(pady=12,padx=12)

    checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12,padx=12)

    label2 = ctk.CTkLabel(master=frame, text="Don't have an account, create a new one here", font=("Roboto", 10), cursor="hand2", text_color= ("#DB3E39", "#821D1A"))
    label2.pack(pady=1, padx=10)
    label2.bind("<Button-1>", lambda event: open_registration_window())  # Bind the click event to open the registration window

    root.mainloop()

open_sign_in()