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
	
def handle_net_names(entry_file,ip,port):

	net_count = 1
	net_id = str(net_count)
	server_address = (ip,port)
	name_dict = {}


	while True:
		request_header_net = 'GET /api/netname/' + net_id + '\rHTTP/1.1\r\nHost: ' + entry_file + '\r\n\n' 
	
		http_response = send_request(request_header_net,server_address)
		status = http_response.split(' ')
		
		net_count = net_count + 1
		net_id = str(net_count)
	
		data_response = http_response.split('\n')
		data = data_response[7].strip(' ') 

		name_dict[net_id] = {data} 

		if data == 'EOF':		#consertar limites
			break

	#----fim while--------------#	
	
	return name_dict
	


def handle_ix_objects(entry_file,ip,port):

	server_address = (ip,port)

	request_header_ix = 'GET /api/ix\rHTTP/1.1\r\nHost:' + entry_file + '\r\n\n'		
	http_response = send_request(request_header_ix, server_address)
		

	take_off_header = http_response.split('"data":')
	take_off_footer = take_off_header[1].split('"meta":')
	
	take_off_footer[0] = take_off_footer[0].replace('[','').replace('],','').replace('\n','').replace(' ','')
	string = take_off_footer[0]

	data_ix = "{" + '"data": [' + string +"] }"
	
	data_ix = json.loads(data_ix)
	
	return data_ix
	
	'''forma de acesso data_ix["data"][i], i: numero correspondente ao ix'''


def handle_ixnets(entry_file,ip,port):
	server_address = (ip,port)

	ix_net = []		
	ix_count = 1
	ix_id = str(ix_count)

	ixnets = {}

	for i in ix_objects["data"]:
		ix_id = str(i["id"])

		request_header_ixnets = 'GET /api/ixnets/' + ix_id + '\rHTTP/1.1\r\nHost: ' + entry_file + '\r\n\n'
		http_response = send_request(request_header_ixnets, server_address)

		take_off_header = http_response.split('"data":')
		take_off_header[1] = take_off_header[1].strip('\n}\n\'')

		str_list = take_off_header[1]
		str_list = str_list.replace('[','').replace(']','').replace('\n','')
		str_list = str_list.replace(' ','')
		str_list = str_list.split(',')


		ixnets[ix_id] = {str(str_list)} 	

	return ixnets	


def handle_data(entry_file,ip,port):
	global net_names
	global ix_objects
	global ix_nets
	
	net_names = handle_net_names(entry_file, ip, port)

	ix_objects = handle_ix_objects(entry_file, ip, port)

	ix_nets = handle_ixnets(entry_file, ip, port) 
	
def analysis_one():
	
	for i in ix_objects["data"]:
		print(i["id"], end = '\t')
		print(i["name_long"], end = '\t')


		string = str(ix_nets[str(i["id"])])
		string = string.replace('{"[','').replace(']"}','')
		string = string.split(',')
		string = list(set(string))
		print(len(string))


def analysis_zero():
	pass

def main():
	entry_file = sys.argv[1]
	if  len(sys.argv) == 3:
		opt = int(sys.argv[2])

	entry = entry_file.split(':')
	ip = entry[0]
	port = int(entry[1])

	handle_data(entry_file,ip,port)

	analysis_one()

if __name__ == '__main__':
	main()






