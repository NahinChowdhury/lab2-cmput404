#!/usr/bin/env python3
import socket, sys, os
import time

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


#get host information
def get_remote_ip(host):
	print(f'Getting IP for {host}')
	try:
		remote_ip = socket.gethostbyname( host )
	except socket.gaierror:
		print ('Hostname could not be resolved. Exiting')
		sys.exit()

	print (f'Ip address of {host} is {remote_ip}')
	return remote_ip



def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	
		#QUESTION 3
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		#bind socket to address
		s.bind((HOST, PORT))
		#set to listening mode
		s.listen(2)
		
		#continuously listen for connections
		while True:
			conn, addr = s.accept()
			print("Connected by", addr)
			
			pid = os.fork()

			if pid == 0:
				full_data = conn.recv(BUFFER_SIZE).decode()
				#recieve data, wait a bit, then send it back
				remote_ip = get_remote_ip("www.google.com")

				googleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				googleSocket.connect((remote_ip , 80))
				
				payload = f"GET /search?q={full_data} HTTP/1.1\r\nHost: www.google.com\r\n\r\n"
				googleSocket.sendall(payload.encode())

				response = googleSocket.recv(BUFFER_SIZE)
				conn.sendall(response)
				conn.close()
				googleSocket.close()
			else:
				conn.close()

if __name__ == "__main__":
	main()
