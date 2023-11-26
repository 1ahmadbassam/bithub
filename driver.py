from frontend import login_module
import caching
import threading
from server import run_server

def exit_script():
    try:
        while True:
            inp = input("[INFO] Type 'exit' to exit\n")
            if inp.strip().lower() == "exit":
                print("[INFO] Server is terminating...")
                break
    except KeyboardInterrupt:
        pass
    caching.save_globals()
    exit(0)

sign_in_thread = threading.Thread(target = login_module.open_sign_in)
sign_in_thread.daemon = True
sign_in_thread.start()
exit_script()