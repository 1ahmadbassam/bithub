# bithub
Proxy server in python

Tools and libraries used:
- Python 3.11
- tkinter and custom tkinter
- os, time, datetime, socket, threading

Resources:
- https://scribe.rip/@miguendes/how-to-check-if-a-string-is-a-valid-url-in-python-fb0584aab549
- https://note.nkmk.me/en/python-os-mkdir-makedirs/
- https://www.tutorialspoint.com/python/os_utime.htm
- https://stackoverflow.com/questions/29792189/grouping-constants-in-python
- https://www.geeksforgeeks.org/min-heap-in-python/
- https://customtkinter.tomschimansky.com/documentation/
- https://builtin.com/data-science/python-socket
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Warning
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-CH
- https://wiki.froth.zone/wiki/List_of_HTTP_header_fields?lang=en#Request_fields

Steps followed:
1) We created our own http library where we created the 2 classes Request and Response that parse the http requests and responses into Request and Responses objects to be able to manipulate them.
2) We created a caching system.
3) We created the user interface using tkinter, customtkinter libraries.
