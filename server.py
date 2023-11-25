import socket
import threading

import caching
from httplib import http
from httplib.requests import Request
from httplib.responses import Response
from reception import recv_all

PORT = 8080
SERVER = ""
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def connect_to_external_server(client_to_origin: socket.socket, req: Request) -> (Response, bytes, bytes):
    if not req.if_modified_since:
        cache_obj, modified = caching.retrieve_from_cache(caching.get_path_from_url(req.path, req.get_obj_filename()))
        if cache_obj:
            req.if_modified_since = (modified, len(cache_obj))
        client_to_origin.send(str(req).encode(http.Charset.ASCII))
        resp, resp_obj = recv_all(client_to_origin, False)
        return_obj = handle_cache_obj(req, resp, cache_obj, resp_obj)
        if resp.status_code == 304:
            resp.status_code = 200
            resp.status_phrase = "OK"
        return resp, return_obj
    else:
        client_modified = req.if_modified_since[0]
        cache_obj, modified = caching.retrieve_from_cache(caching.get_path_from_url(req.path, req.get_obj_filename()))
        if cache_obj:
            req.if_modified_since = (modified, len(cache_obj))
        client_to_origin.send(str(req).encode(http.Charset.ASCII))
        resp, resp_obj = recv_all(client_to_origin, False)
        return_obj = handle_cache_obj(req, resp, cache_obj, resp_obj)
        if resp.last_modified[0] > client_modified:
            return resp, return_obj
        else:
            resp.status_code = 304
            resp.status_phrase = "Not Modified"
            print(f"[INFO] Client already has up-to-date object {req.path}.")
            return resp, b''


def handle_cache_obj(req: Request, resp: Response, cache_obj: bytes, resp_obj: bytes) -> bytes:
    filename = req.get_obj_filename()
    if resp.status_code == 200 and "no-store" not in resp.cache_control:
        caching.add_to_cache(caching.get_path_from_url(req.path, filename), filename, resp_obj, resp.last_modified[0])
    elif resp.status_code == 304:
        print(f"[INFO] Object {req.path} not modified.")
        print(f"[INFO] Object retrieved from cache.")
        return cache_obj
    elif "no-store" in resp.cache_control:
        pass
    else:
        print("[INFO] Cannot cache object for response with status " + str(resp.status_code) + " "
              + str(resp.status_phrase) + ".")
        print("[INFO] URL of problem is " + req.path)
    return resp_obj


def handle_client(conn: socket.socket, addr: str) -> None:
    print(f"[INFO] Client with address {addr} has initiated a connection.")
    connected = True
    client_to_origin = None
    while connected:
        connected = False
        try:
            req, req_obj = recv_all(conn)
            if not req:
                continue
            if req.command == Request.Command.POST:
                break
            print(req)
            client_to_origin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_to_origin.connect((req.host, 80))
            resp, obj = connect_to_external_server(client_to_origin, req)
            if "keep-alive" in req.connection and "keep-alive" in resp.connection:
                connected = True

            else:
                resp.connection = {"close"}
            print(resp)
            print(str(resp).encode(http.Charset.ASCII) + obj)
            conn.send(str(resp).encode(http.Charset.ASCII) + obj)
        except (ConnectionError, ConnectionResetError):
            break
        except Exception as e:
            raise e
    if client_to_origin:
        client_to_origin.close()
    conn.close()
    print(f"[INFO] Client with address {addr} has terminated a connection.")


def run_server():
    caching.load_globals()
    server.listen(10)  # process 10 connections at a time maximum
    print(f"[INFO] Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        conn_thread = threading.Thread(target=handle_client, args=(conn, addr))
        conn_thread.start()


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


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    exit_script()
