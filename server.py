# Python program to implement server side of chat room.
import socket
import select
import sys
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 4:
	print "Correct usage: script, IP address, port number, username"
	exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
username = str(sys.argv[3])
server.bind((IP_address, Port))
server.listen(100)
list_of_clients = []

def converter(s):
	new = ""
	for x in s:
		new += x
	return new

def clientthread(conn, addr):
	conn.send("Welcome to this chatroom!")
	clientname = conn.recv(2048)
	while True:
			try:
				mes = ''
				message = conn.recv(2048)
				if message:
					print "<" + addr[0] + "," + clientname + "> " + message
					for i in range(len(message)):
						mes += chr(ord(message[i])-1)
					message = converter(mes)
					print "<" + addr[0] + "," + clientname + "> " + message
					message_to_send = "<" + addr[0] + "," + clientname + "> " + message
					broadcast(message_to_send, conn)
				else:
					remove(conn)

			except:
				continue

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message)
			except:
				clients.close()
				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print addr[0] + " connected"
	start_new_thread(clientthread, (conn,addr))

conn.close()
server.close()


	# for socks in read_sockets:
	# 		message = sys.stdin.readline()
	# 		server.send(message)
	# 		sys.stdout.write("<You>")
	# 		sys.stdout.write(message)
	# 		sys.stdout.flush()
