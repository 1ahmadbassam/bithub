import socket

from httplib import http
from httplib.requests import __parse_http_line as parse_http_line, parse as parse_request
from httplib.responses import parse as parse_response

BUFFER = 2 << 11
INITIAL_LENGTH = 2 << 13


timeout = 2


def set_timeout(val: float):
    global timeout
    timeout = val


def get_data_from_chunked(bytestream: bytes, trailer: bool = False) -> (bytes, bool, bytes):
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
        data += bytestream[i:i + cl + 1]
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
    try:
        initial_bytestream = sock.recv(INITIAL_LENGTH)
    except TimeoutError:
        print("[INFO] Timed out.")
        return None, None
    if initial_bytestream:
        sock.settimeout(timeout)
        header, initial_data = get_initial_data_bytestream(initial_bytestream)
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
            primary_obj.transfer_encoding = None
            primary_obj.content_length = len(data)
        elif primary_obj.content_length:
            data = initial_data
            data += recv_content_length_data(sock, int(primary_obj.content_length))
        else:
            data = initial_data
            data += recv_data(sock)
        return primary_obj, data
    return None, None


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
