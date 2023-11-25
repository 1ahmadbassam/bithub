import socket
import threading

import caching
from httplib import http
from httplib.requests import Request
from httplib.requests import __parse_http_line as parse_http_line, parse as parse_request
from httplib.responses import Response
from httplib.responses import parse as parse_response

PORT = 8080
SERVER = ""
ADDR = (SERVER, PORT)
BUFFER = 2 << 11
INITIAL_LENGTH = 2 << 13
TIMEOUT = 2

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def get_data_from_chunked(bytestream: bytes, trailer: bool = False) -> (bytes, bool, bytes):
    print(bytestream)
    curr_length = 0
    data = b''
    i = 0
    while curr_length < len(bytestream):
        cl = []
        while i < len(bytestream):
            char = bytestream[i].to_bytes().decode(http.Charset.ASCII)
            if char == '\r':
                break
            cl.append(char)
            i += 1
        i += 1
        cl = int(''.join(cl), 16)
        if cl == 0 and trailer:
            trailer_data = bytestream[i:-2]
            return data, False, trailer_data
        elif cl == 0:
            return data, False, None
        data += bytestream[i:i + cl]
        i += cl + 2
    return data, True, None


def recv_transfer_encoding_data(sock: socket.socket, trailer: bool = False) -> (bytes, bytes):
    resume = True
    data = b''
    trailer_data = None
    while resume:
        try:
            bytestream = sock.recv(BUFFER)
            if len(bytestream) == 0:
                break
            data_chunk, resume, trailer_data = get_data_from_chunked(bytestream, trailer)
            data += data_chunk
        except TimeoutError:
            break
    return data, trailer_data


def recv_content_length_data(sock: socket.socket, length: int) -> bytes:
    remaining = length
    data = b''
    while remaining > 0:
        try:
            part = sock.recv(BUFFER)
            if len(part) == 0:
                break
            remaining -= len(part)
            data += part
        except TimeoutError:
            break
    return data


def recv_data(sock: socket.socket) -> bytes:
    data = b''
    while True:
        try:
            part = sock.recv(BUFFER)
            if len(part) == 0:
                break
            data += part
        except TimeoutError:
            break
    return data


def recv_all(sock: socket.socket, request: bool = True):
    bytestream = sock.recv(INITIAL_LENGTH)
    if bytestream:
        sock.settimeout(TIMEOUT)
        header, initial_data = get_initial_data_bytestream(bytestream)
        # get request/response obj
        if request:
            primary_obj = parse_request(header)
        else:
            primary_obj = parse_response(header)
        if primary_obj.transfer_encoding and "chunked" in primary_obj.transfer_encoding:
            if primary_obj.trailer:
                data, resume, trailer = get_data_from_chunked(initial_data, True)
            else:
                data, resume, trailer = get_data_from_chunked(initial_data)
            if resume:
                if primary_obj.trailer:
                    part, trailer = recv_transfer_encoding_data(sock, True)
                else:
                    part, trailer = recv_transfer_encoding_data(sock)
                data += part
            if trailer:
                primary_obj.trailer = set()
                trailer = trailer.decode(http.Charset.ASCII)
                for line in trailer.split(http.DELIMITER):
                    parse_http_line(line, primary_obj)
        elif primary_obj.content_length:
            data = initial_data
            data += recv_content_length_data(sock, int(primary_obj.content_length))
        else:
            data = initial_data
            data += recv_data(sock)
        bytestream += data
        return primary_obj, data, bytestream
    return None, None, None


def get_initial_data_bytestream(bytestream: bytes) -> (str, bytes):
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


def connect_to_external_server(req: Request) -> (Response, bytes, bytes):
    client_to_origin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_to_origin.connect((req.host, 80))
    client_to_origin.send(str(req).encode(http.Charset.ASCII))
    resp, obj, bytestream = recv_all(client_to_origin, False)
    print(resp)
    handle_cache_obj(req, resp, obj)
    return resp, obj, bytestream


def handle_cache_obj(req: Request, resp: Response, obj: bytes) -> None:
    filename = req.get_obj_filename()
    if resp.status_code == 200:
        caching.add_to_cache(caching.get_path_from_url(req.path, filename), filename, obj)
    else:
        print("[INFO] Cannot cache object for response with status " + str(resp.status_code) + " "
              + str(resp.status_phrase) + ".")
        print("[INFO] URL of problem is " + req.path)


def handle_client(conn: socket.socket, addr: str) -> None:
    print(f"[INFO] Client with address {addr} has initiated a connection.")
    connected = True
    sock_open = True
    while connected:
        connected = False
        try:
            req, req_obj, req_bytestream = recv_all(conn)
            print(req)
            if req_bytestream:
                resp, obj, bytestream = connect_to_external_server(req)

                if "keep-alive" in req.connection and "keep-alive" in resp.connection:
                    connected = True
                else:
                    resp.connection = {"close"}
                conn.send(bytestream)
        except (ConnectionError, ConnectionResetError):
            sock_open = False
            conn.close()
            print(f"[INFO] Client with address {addr} has terminated a connection.")
            break
        except Exception as e:
            conn.close()
            print(f"[INFO] Client with address {addr} has terminated a connection.")
            raise e
    if sock_open:
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
