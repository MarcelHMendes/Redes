#!/usr/bin/python
# -*- coding: utf-8 -*-

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

import socket, sys, json

entry_file = sys.argv[1]
if  len(sys.argv) == 3:
	opt = sys.argv[2]

entry = entry_file.split(':')
ip = entry[0]
port = int(entry[1])

#client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = (ip, port)
#client_sock.connect(server_address)


net_count = 1
net_id = str(net_count)

while True:
	request_header_net = 'GET /api/netname/' + net_id + '\rHTTP/1.1\r\nHost: ' + entry_file + '\r\n\n' 
	print(request_header_net)
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (ip, port)
	client_sock.connect(server_address)

	client_sock.send(request_header_net.encode())

	response = ''

	while True:
		recv = client_sock.recv(1024)
		if not recv:
			break
		response += recv.decode()

	client_sock.close()

	#response = response.split(' ')
	
	net_count = net_count + 1
	net_id = str(net_count)

	



