import socket
import threading
from requests import Request, parse

PORT = 8080
SERVER =  socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
BUFFER = 2 << 11
ACCEPT_LENGTH = 2 << 13

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
	print(f"[INFO] Client with address {addr} has initiated a connection.")
	while True:
		try:
			req = conn.recv(ACCEPT_LENGTH)
			if req:
				r = parse(req.decode(Request.ASCII))
				print(r)
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
