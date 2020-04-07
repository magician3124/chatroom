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
mes = ''
temp = 0

def converter(s):
	new = ""
	for x in s:
		new += x
	return new

while True:
	sockets_list = [sys.stdin, server]
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			print message
		else:
			message = sys.stdin.readline()
			for i in range(len(message)):
				temp = ord(message[i])+i
				if(temp > 127):
					temp -= 128
				mes += chr(temp)
			server.send(converter(mes))
			sys.stdout.write("<" + username + ">")
			# sys.stdout.write(message)
			sys.stdout.flush()
			mes = ""
server.close()
