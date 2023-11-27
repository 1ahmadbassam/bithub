import socket
import threading
import time
from datetime import datetime

import caching
import security
from httplib import http
from httplib.requests import Request
from httplib.responses import Response
from reception import recv_all, set_timeout, timeout

PORT = 8080
SERVER = ""
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def connect_to_external_server(client_to_origin: socket.socket, req: Request) -> (Response, bytes, bytes):
    """
        This function is responsible for connecting to external servers as requested by clients.
    """
    if not req.if_modified_since:  # caching: check if obj already exists on the client side
        # check if obj exists in our cache
        cache_obj, modified = caching.retrieve_from_cache(caching.get_path_from_url(req.path, req.get_obj_filename()))
        if cache_obj:  # if yes, send an if_modified_since based on our cache's last modified
            # this is achieved by helper functions in the caching module
            req.if_modified_since = (modified, len(cache_obj))
        # send request to origin server
        client_to_origin.send(str(req).encode(http.Charset.ASCII))
        print(f"[INFO] Sent a request to host {req.host} at {http.get_date_string(datetime.now())}")
        # retrieve response from origin server
        resp, resp_obj = recv_all(client_to_origin, False)
        print(f"[INFO] Received a response from host {req.host} at {http.get_date_string(datetime.now())}")
        # handle caching status, let caching method return us the correct object to forward to client
        return_obj = handle_cache_obj(req, resp, cache_obj, resp_obj)
        if resp.status_code == 304:  # if we get a 304, this is for us; the client doesn't have this in his cache
            resp.status_code = 200
            resp.status_phrase = "OK"
        return resp, return_obj
    else:
        client_modified = req.if_modified_since[0]
        # caching: the client has a file modified date
        # of the one specified in the if-modified since header field
        # the rest is same as above
        cache_obj, modified = caching.retrieve_from_cache(caching.get_path_from_url(req.path, req.get_obj_filename()))
        if cache_obj:
            req.if_modified_since = (modified, len(cache_obj))
        client_to_origin.send(str(req).encode(http.Charset.ASCII))
        print(f"[INFO] Sent a request to host {req.host} at {http.get_date_string(datetime.now())}")
        resp, resp_obj = recv_all(client_to_origin, False)
        print(f"[INFO] Received a response from host {req.host} at {http.get_date_string(datetime.now())}")
        return_obj = handle_cache_obj(req, resp, cache_obj, resp_obj)
        if resp.last_modified[0] > client_modified:  # if we have found a newer obj than the client's one just send
            return resp, return_obj
        else:  # in this part however, the difference is that the client has the object. just forward a 304 to him.
            resp.status_code = 304
            resp.status_phrase = "Not Modified"
            print(f"[INFO] Client already has up-to-date object {req.path}.")
            return resp, b''


def handle_cache_obj(req: Request, resp: Response, cache_obj: bytes, resp_obj: bytes) -> bytes:
    """
        This function is responsible for handling cached objects on the server side,
         which relies on properties provided by the caching module.
    """
    filename = req.get_obj_filename()  # required for caching module
    # if the file can be cached, then add it to the global cache
    if resp.status_code == 200 and "no-store" not in resp.cache_control:
        caching.add_to_cache(caching.get_path_from_url(req.path, filename), filename, resp_obj,
                             resp.last_modified[0] if resp.last_modified else datetime.now())
    elif resp.status_code == 304:  # the object is not modified, so just confirm the one from cache
        print(f"[INFO] Object {req.path} not modified.")
        print(f"[INFO] Object retrieved from cache.")
        return cache_obj
    # if the object cannot be cached because it has been specified as such, then pass
    elif "no-store" in resp.cache_control:
        pass
    else:  # some error occurred. do not cache the file as it may be an error document by the server
        print("[INFO] Cannot cache object for response with status " + str(resp.status_code) + " "
              + str(resp.status_phrase) + ".")
        print("[INFO] URL of problem is " + req.path)
    return resp_obj


def handle_client(conn: socket.socket, addr: str, users_ip: dict) -> None:
    """
        This function is responsible for handling a connecting client
        which is running in its own thread for each connection.
    """
    print(f"[INFO] Client with address {addr} has initiated a connection.")
    connected = True
    client_to_origin = None
    start_time = 0
    while connected:  # while the connection is keep-alive, do the following
        connected = False  # assume that the connection is close
        try:
            req, req_obj = recv_all(conn)  # attempt to receive any data from request through a special fn
            if not req:
                continue
            if req.command == Request.Command.POST:
                # POSTs aren't implemented yet (even though we do acquire the request object)
                break
            print(f"[INFO] Received a request from {addr[0]} at {http.get_date_string(datetime.now())}")
            print(req)
            if req.host in security.BLOCKED_HOSTNAMES:
                # if this host is forbidden, then must send blocked HTML instead of actual response to client
                # as we are not interested in connecting to blocked websites
                # simply send a 403 forbidden response, with the response object being our custom html
                resp = Response(403, "Forbidden")
                resp.connection = {"close"}
                obj = security.load_blocking_html()
                resp.content_length = len(obj)
                print(resp)
                conn.send(str(resp).encode(http.Charset.ASCII) + obj)
                break
            elif req.host in security.SECURED_WEBSITES and req.proxy_authorization:
                # if the desired website is secured (e.g. intranet website),
                # the client must authorize the access to this website
                # to do so, the client must authorize on his browser with valid credentials
                credentials = req.get_base64_encoded_proxy_credentials()
                if credentials and security.authenticate(req.get_base64_encoded_proxy_credentials().encode()):
                    # if credentials are valid, then simply skip, as the website could be loaded normally
                    # the credentials are checked by a helper method in the security namespace
                    pass
                else:
                    # send a 407 response to ask for credentials if they are not found or invalid
                    resp = Response(407, "Proxy Authentication Required", http.Version.HTTP11)
                    resp.connection = {"close"}
                    resp.proxy_authenticate = 'Basic realm="This website is protected"'
                    print(resp)
                    conn.send(str(resp).encode(http.Charset.ASCII))
                    break
            elif req.host in security.SECURED_WEBSITES:
                # send a 407 response to ask for credentials if they are not found or invalid
                resp = Response(407, "Proxy Authentication Required", http.Version.HTTP11)
                resp.connection = {"close"}
                resp.proxy_authenticate = 'Basic realm="This website is protected"'
                print(resp)
                conn.send(str(resp).encode(http.Charset.ASCII))
                break
            if not client_to_origin or (start_time and time.time() - start_time < timeout):
                # timeout occurred, be sure to close the socket to prevent sending issues
                if client_to_origin:
                    client_to_origin.close()
                # if the socket is invalid, then create it
                # else, the socket has been saved from previous sessions
                # just check if the connection has timed out and it should be closed
                client_to_origin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_to_origin.connect((req.host, 80))
                set_timeout(2)
                start_time = 0
            # retrieve a response and an object from a specialized function which handles retrieving from origin servers
            resp, obj = connect_to_external_server(client_to_origin, req)
            if "keep-alive" in req.connection and "keep-alive" in resp.connection:
                # the connection is keep alive, thus, must keep socket to origin server open
                # and appropriately time it, so it times out in case of any issue
                connected = True
                if resp.keep_alive and isinstance(resp.keep_alive, dict) and "timeout" in resp.keep_alive:
                    set_timeout(resp.keep_alive[0])
                elif resp.keep_alive and isinstance(resp.keep_alive, str):
                    set_timeout(int(resp.keep_alive))
                else:
                    set_timeout(5)
            else:
                # else, the connection must be closed.
                # close the connection by setting the respective parameters
                resp.connection = {"close"}
                set_timeout(2)
                start_time = 0
                connected = False
            print(resp)
            # report to admin in case of any error from origin server in response
            if resp.status_code != 200 and resp.status_code != 304:
                print(f"[INFO] The HTTP origin server has responded with an error "
                      f"{resp.status_code} {resp.status_phrase} for the request of the client "
                      f"{addr[0]} at {http.get_date_string(datetime.now())}")
            conn.send(str(resp).encode(http.Charset.ASCII) + obj)
            print(f"[INFO] Sent a response to {addr[0]} at {http.get_date_string(datetime.now())}")
            # send back to the client the modified response and the requested object

            # at this point, the loop will occur if keep-alive is valid
        except (ConnectionError, ConnectionResetError):
            # these errors indicate that the connection has been weirdly terminated, so simply stop
            break
        except Exception as e:
            # if any exception occurs, due to incorrect logic
            # or unpredictable situations, be sure to throw them to notify the user
            raise e
    # if this socket is still open then definitely close it
    # most likely the connection was 'close' from the client end but 'keep-alive' from the server end
    if client_to_origin:
        client_to_origin.close()
    conn.close()
    print(f"[INFO] Client with address {addr} has terminated a connection.")
    # one less connection for this user, and remove his ip address if he doesn't have any more open connections
    # to save memory, we do not keep track of the users log beyond the number of open connections they have
    users_ip[addr[0]] -= 1
    if users_ip[addr[0]] == 0:
        users_ip.pop(addr[0])


def run_server():
    """
        This function is responsible for starting the server.
    """
    caching.load_globals()  # load caching globals (size, minheap, dictionary)
    server.listen(50)  # process 50 connections at a time maximum
    print(f"[INFO] Server is listening on {ADDR}")
    users_ip = {}
    while True:  # accept incoming connections all the time (wait for them)
        conn, addr = server.accept()  # accept this connection to inspect its properties
        if addr[0] in security.BLOCKED_IP_ADDRESSES:  # if this connection is blacklisted, then it is immediately
            # terminated
            print(f"[SECURITY] Blocked IP address in blacklist {addr[0]}")
            conn.close()
        elif (addr[0] in users_ip
              and users_ip[addr[0]] == 5):  # if this host has already established 5 connections, then block him from
            # creating more
            print(f"[SECURITY] Blocked IP address with excessive connections {addr[0]}")
            conn.close()
        else:  # else, host is OK
            if addr[0] not in users_ip:  # first-time connection
                users_ip[addr[0]] = 1
            else:  # add an incoming connection
                users_ip[addr[0]] += 1
            conn_thread = threading.Thread(target=handle_client, args=(conn, addr, users_ip))
            # open a thread for this client
            conn_thread.start()


if __name__ == "__main__":
    # run command-line based version of the server if this file is executed
    run_server()
