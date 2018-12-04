#!/usr/bin/python
# -*- coding: utf-8 -*-

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

import socket, sys, json


def send_request(request_header,server_address):
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_sock.connect(server_address)

	client_sock.send(request_header.encode())

	response = ''

	while True:
		recv = client_sock.recv(1024)
		if not recv:
			break
		response += recv.decode()
			
	client_sock.close()
	return response
	


def analise_zero(entry_file,ip,port):
	net_count = 1
	net_id = str(net_count)
	server_address = (ip,port)
	name_dict = {}

	'''while True:
		request_header_net = 'GET /api/netname/' + net_id + '\rHTTP/1.1\r\nHost: ' + entry_file + '\r\n\n' 
		print(request_header_net)
		http_response = send_request(request_header_net,server_address)
		status = http_response.split(' ')
		
		net_count = net_count + 1
		net_id = str(net_count)
	
		data_response = http_response.split('\n')
		data = data_response[7].strip(' ') 

		name_dict[net_id] = {data} 

		if data == 'EOF':		#consertar limites
			break
	'''
	#----fim while--------------#	
	

	ix_count = 2
	ix_id = str(ix_count)
	
	request_header_ixnets = 'GET /api/ixnets/' + ix_id + '\rHTTP/1.1\r\nHost: ' + entry_file + '\r\n\n'
	print(request_header_ixnets)
	http_response = send_request(request_header_ixnets, server_address)

	take_off_header = http_response.split('"data":')
	take_off_header[1] = take_off_header[1].strip('\n}\n\'')

	str_list = take_off_header[1]
	str_list = str_list.replace('[','').replace(']','').replace('\n','')
	str_list = str_list.replace(' ','')
	str_list = str_list.split(',')

	print(str_list)	

		
def main():
	entry_file = sys.argv[1]
	if  len(sys.argv) == 3:
		opt = sys.argv[2]

	entry = entry_file.split(':')
	ip = entry[0]
	port = int(entry[1])

	
	analise_zero(entry_file,ip,port)

if __name__ == '__main__':
	main()







'''request_header_ix = 'GET /api/ix\rHTTP/1.1\r\nHost:' + entry_file + '\r\n\n'		
	http_response = send_request(request_header_ix, server_address)
	print(http_response)'''
		