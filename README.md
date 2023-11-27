# bithub
Proxy server in python

Tools and libraries used:
- Python 3.11
- tkinter and custom tkinter
- os, time, datetime, socket, threading
- pickle

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

Extra Features:
- Complete and fail-proof parsing of request headers and response headers into Request and Response header objects with most header fields found in modern and old http requests with their correct corresponsing types. The reason is for easier reception and manipulation of different forms of requests and responses as well as changing the headers of these requests and responses.
- Users can send HTTP requests directly from browsers and without the need for a client side.
- Caching directly onto computer disk and persisting the cache between proxy sessions.
- Implementing the Least Recently Used (LRU) algorithm using a minimum-heap and a dictionary for fast efficient caching.
- Limitations and accomodations of implementations:
  - a maximum of 50 global concurrent connections at a time 
  - a maximum of 5 connections per host at a time
  - a maximum of 10 hosts using the server at the same time
- Implemented a graphical user interface that displays all required and additional information.
- To secure and access the GUI, administrators must create an account and authenticate their sign in which is done using a secure hashing system.
- Users can choose to run the proxy server as well as exist and terminate the proxy server without the need for terminal/cmd interference.
- Handle all file types, ex: html, gif, css, any binary object.
- Handling cases of cache control: no-cache, no-store.
- Handling all reception types: chunked, with content length, with nothing => timeout w hal 5bar
- 