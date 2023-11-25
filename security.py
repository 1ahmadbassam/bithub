BLOCKING_HTML = "blocked.html"

BLOCKED_IP_ADDRESSES = {"172.20.10.3"}
BLOCKED_HOSTNAMES = {"steptail.com", "www.google.com", "www.microsoft.com"}

SECURED_WEBSITES = {"frogfind.com"}


def load_blocking_html():
    with open(BLOCKING_HTML, "rb") as file:
        return file.read()
