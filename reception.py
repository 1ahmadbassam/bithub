import socket

from httplib import http
from httplib.requests import __parse_http_line as parse_http_line, parse as parse_request
from httplib.responses import parse as parse_response

BUFFER = 2 << 11
INITIAL_LENGTH = 2 << 13


timeout = 2


def set_timeout(val: float):
    '''
        Set the timeout for the socket.
    '''
    global timeout
    timeout = val


def get_data_from_chunked(bytestream: bytes, trailer: bool = False) -> (bytes, bool, bytes):
    '''
        Get the data from the chunked bytestream.
    '''
    curr_length = 0
    data = b''
    i = 0
    while curr_length < len(bytestream): # while the current length is less than the length of the bytestream, there is still data to be read
        cl = []
        while i < len(bytestream): # while the index is less than the length of the bytestream, there is still data to be read
            char = bytestream[i].to_bytes().decode(http.Charset.ASCII) # convert the byte to a character
            if char == '\r': # if the character is a carriage return, break
                break
            cl.append(char)
            i += 1
        i += 1
        cl = int(''.join(cl), 16) # in chunking, a hexadecimal number representing the number of bytes in the trailer, convert the hexadecimal string to an integer
        if cl == 0 and trailer:
            trailer_data = bytestream[i:-2]
            return data, False, trailer_data 
        elif cl == 0:
            return data, False, None
        data += bytestream[i:i + cl + 1] # add the data to the data variable
        i += cl + 2
    return data, True, None # return the data, whether or not there is more data to be read, and the trailer data


def recv_transfer_encoding_data(sock: socket.socket, trailer: bool = False) -> (bytes, bytes):
    '''
        Receive the data from the socket if there is transfer encoding field.
    '''
    resume = True
    data = b''
    trailer_data = None
    while resume: # while there are more chunks that will be sent
        try:
            bytestream = sock.recv(BUFFER) 
            if len(bytestream) == 0: # if the length of the previous bytestream is 0, break
                break
            data_chunk, resume, trailer_data = get_data_from_chunked(bytestream, trailer) # get the data from the chunked bytestream
            data += data_chunk
        except TimeoutError: # account for timeout errors
            break
    return data, trailer_data # return the data and the trailer data


def recv_content_length_data(sock: socket.socket, length: int) -> bytes:
    '''
        Receive the data from the socket if there is content length field.
    '''
    remaining = length
    data = b''
    while remaining > 0:
        try:
            part = sock.recv(BUFFER) # receive the data from the socket
            if len(part) == 0:
                break
            remaining -= len(part)
            data += part
        except TimeoutError: # account for timeout errors
            break
    return data


def recv_data(sock: socket.socket) -> bytes:
    '''
        Receive the data from the socket. This is the default case where we dont have chiunks or content length.
    '''
    data = b''
    while True:
        try:
            part = sock.recv(BUFFER) # receive the data from the socket
            if len(part) == 0:
                break
            data += part
        except TimeoutError: # account for timeout errors
            break
    return data


def recv_all(sock: socket.socket, request: bool = True):
    '''
        Receive all the data from the socket whether it be chunked, content length, or default.
    '''
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
        if primary_obj.transfer_encoding and "chunked" in primary_obj.transfer_encoding: # if there is a transfer encoding field and it is chunked
            if primary_obj.trailer:
                data, resume, trailer = get_data_from_chunked(initial_data, True)
            else: 
                data, resume, trailer = get_data_from_chunked(initial_data)
            if resume: # if there is more data to be read
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
    '''
        Get the initial data from the bytestream.
    '''
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
