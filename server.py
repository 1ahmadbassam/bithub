import socket
import threading

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def recv_all(sock):
    data = b''
    while True:
        part = sock.recv(BUFFER)
        if len(part) == 0:
            break
        data += part
    return data


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
    return header, obj


def connect_to_external_server(req):
    client_to_origin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_to_origin.connect((req.host, 80))
    client_to_origin.send(str(req).encode(http.Charset.ASCII))
    data = recv_all(client_to_origin)
    header, obj = get_data_from_byte_stream(data)
    resp = parse_response(header)
    print(resp)
    return resp, obj


def handle_cache_obj(req: Request, resp: Response, obj: bytes):
    filename = req.get_obj_filename()
    if resp.status_code == "200":
        caching.add_to_cache(caching.get_path_from_url(req.path, filename), int(resp.content_length), filename, obj)
    else:
        print("[INFO] Cannot cache object for response with status " + str(resp.status_code) + " "
              + str(resp.status_phrase) + ".")
        print("[INFO] URL of problem is " + req.path)


def handle_client(conn, addr):
    print(f"[INFO] Client with address {addr} has initiated a connection.")
    while True:
        try:
            req_bytes = conn.recv(ACCEPT_LENGTH)
            if req_bytes:
                req = parse_request(req_bytes.decode(http.Charset.ASCII))
                print(str(req).encode(http.Charset.ASCII))
                resp, obj = connect_to_external_server(req)
                handle_cache_obj(req, resp, obj)
                conn.send(obj)
                conn.close()
                print(f"[INFO] Client with address {addr} has terminated a connection.")
                break
        except (ConnectionError, ConnectionResetError):
            conn.close()
            print(f"[INFO] Client with address {addr} has terminated a connection.")
            break


def run_server():
    server.listen(10)  # process 10 connections at a time maximum
    print(f"[INFO] Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        conn_thread = threading.Thread(target=handle_client, args=(conn, addr))
        conn_thread.start()


if __name__ == "__main__":
    run_server()
