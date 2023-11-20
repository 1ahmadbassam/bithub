import socket
import threading
from requests import Request
from requests import parse as parse_request
from responses import parse as parse_response

PORT = 8080
SERVER = ""
ADDR = (SERVER, PORT)
BUFFER = 2 << 11
ACCEPT_LENGTH = 2 << 13

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def recv_all(sock):
	buf_size = 4096
	data = b''
	while True:
		part = sock.recv(buf_size)
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
		char = bytestream[i].to_bytes().decode(Request.ASCII)
		if char == '\r' and prev1 == '\n' and prev2 == '\r':
			break
		header.append(char)
		prev2 = prev1
		prev1 = char
		i += 1
	i += 2
	header.append(Request.DELIMITER)
	header = ''.join(header)
	obj = bytestream[i:]
	return header, obj


def connect_to_external_server(req):
	client_to_origin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_to_origin.connect((req.host, 80))
	client_to_origin.send(str(req).encode(Request.ASCII))
	data = recv_all(client_to_origin)
	header, obj = get_data_from_byte_stream(data)
	header_obj = parse_response(header)
	return header_obj, obj


def handle_client(conn, addr):
	print(f"[INFO] Client with address {addr} has initiated a connection.")
	while True:
		try:
			req = conn.recv(ACCEPT_LENGTH)
			if req:
				r = parse_request(req.decode(Request.ASCII))
				header_obj, obj = connect_to_external_server(r)
				conn.send(obj)
				conn.close()
				print(f"[INFO] Client with address {addr} has terminated a connection.\n{header_obj}")
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
