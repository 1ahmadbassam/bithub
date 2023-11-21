import socket
import threading
import time

from httplib import http
from httplib.requests import parse as parse_request
from httplib.requests import Request
from httplib.responses import parse as parse_response
from httplib.responses import Response

import caching

PORT = 8080
SERVER = ""
ADDR = (SERVER, PORT)
BUFFER = 2 << 11
ACCEPT_LENGTH = 2 << 13
TIMEOUT = 2

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def recv_all(sock):
    bytestream = b''
    while True:
        try:
            sock.settimeout(TIMEOUT)
            part = sock.recv(BUFFER)
            bytestream += part
        except TimeoutError:
            break
    return bytestream


def get_data_from_byte_stream(bytestream):
    prev1 = None
    prev2 = None
    i = 0
    header = []
    while i < len(bytestream):
        char = bytestream[i].to_bytes().decode(http.Charset.ASCII)
        if char == '\r' and prev1 == '\n' and prev2 == '\r':
            break
        header.append(char)
        prev2 = prev1
        prev1 = char
        i += 1
    i += 2
    header.append(http.DELIMITER)
    header = ''.join(header)
    obj = bytestream[i:]
    if not obj:
        obj = b''
    return header, obj


def connect_to_external_server(req):
    client_to_origin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_to_origin.connect((req.host, 80))
    client_to_origin.send(str(req).encode(http.Charset.ASCII))
    bytestream = recv_all(client_to_origin)
    resp, obj = get_data_from_byte_stream(bytestream)
    resp = parse_response(resp)
    print(resp)
    return resp, obj, bytestream


def handle_cache_obj(req: Request, resp: Response, obj: bytes):
    filename = req.get_obj_filename()
    if resp.status_code == "200":
        caching.add_to_cache(caching.get_path_from_url(req.path, filename), filename, obj)
    else:
        print("[INFO] Cannot cache object for response with status " + str(resp.status_code) + " "
              + str(resp.status_phrase) + ".")
        print("[INFO] URL of problem is " + req.path)


def handle_client(conn, addr):
    print(f"[INFO] Client with address {addr} has initiated a connection.")
    connected = True
    while connected:
        connected = False
        try:
            bytestream = recv_all(conn)
            req = get_data_from_byte_stream(bytestream)[0]
            print(req)
            req = parse_request(req)
            if bytestream:
                resp, obj, bytestream = connect_to_external_server(req)
                handle_cache_obj(req, resp, obj)
                if "keep-alive" in req.connection and "keep-alive" in resp.connection:
                    connected = True
                else:
                    resp.connection = {"close"}
                conn.send(bytestream)
                print(f"[INFO] Client with address {addr} has terminated a connection.")
        except (ConnectionError, ConnectionResetError):
            conn.close()
            print(f"[INFO] Client with address {addr} has terminated a connection.")
            break
    conn.close()
    print(f"[INFO] Client with address {addr} has terminated a connection.")


def run_server():
    server.listen(10)  # process 10 connections at a time maximum
    print(f"[INFO] Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        conn_thread = threading.Thread(target=handle_client, args=(conn, addr))
        conn_thread.start()


if __name__ == "__main__":
    run_server()
