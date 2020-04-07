# Python program to implement client side of chat room.
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 4:
	print "Correct usage: script, IP address, port number, username"
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
username = str(sys.argv[3])
server.connect((IP_address, Port))
server.send(username)

while True:
	sockets_list = [sys.stdin, server]
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			print message
		else:
			message = sys.stdin.readline()
			server.send(message)
			sys.stdout.write("<" + username + ">")
			sys.stdout.write(message)
			sys.stdout.flush()
server.close()
