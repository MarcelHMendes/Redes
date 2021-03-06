#!/usr/bin/python
# -*- coding: utf-8 -*-

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

import socket, sys, json


def send_request(request_header,server_address):

	'''Responsavel por estabelecer a conexao e receber os dados
		@return: raw-bytes	

	'''

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

	'''Responsavel por tratar os dados dos nomes das redes 
		@return: dict
		@server_adress: tuple
		@net_id: string
		@name_dict: dict
		@data_response: string

	'''

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
	
	'''Responsavel por lidar com os objetos ix's 
		@return: json
		@request_header: string
		@http_response: raw bytes
		@take_off_footer: string
		@take_off_header: string
	'''

	server_address = (ip,port)

	request_header_ix = 'GET /api/ix\rHTTP/1.1\r\nHost:' + entry_file + '\r\n\n'		
	http_response = send_request(request_header_ix, server_address)
		

	take_off_header = http_response.split('"data":')
	take_off_footer = take_off_header[1].split('"meta":')
	
	take_off_footer[0] = take_off_footer[0].replace('[','').replace('],','').replace('\n','')#.replace(' ','') : bug
	string = take_off_footer[0]

	data_ix = "{" + '"data": [' + string +"] }"
	
	data_ix = json.loads(data_ix)
	
	return data_ix
	
	'''forma de acesso data_ix["data"][i], i: numero correspondente ao ix'''


def handle_ixnets(entry_file,ip,port):
	'''Responsavel por tratar os dados da associacao ix_net 
		@return: dict
		@request_header: string
		@http_response: raw bytes
		@take_off_footer: string
		@take_off_header: string
	 '''

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
	
	'''Responsavel por recolher os dados dos tres endpoints
	'''

	global net_names
	global ix_objects
	global ix_nets
	
	net_names = handle_net_names(entry_file, ip, port)

	ix_objects = handle_ix_objects(entry_file, ip, port)

	ix_nets = handle_ixnets(entry_file, ip, port) 
	
def analysis_one():
	
	'''Responsavel por realizar e imprimir em arquivo a analise um 
		@string: string
		@string: list
	'''
	
	output_one = open('analise_um.tsv','w')

	for i in ix_objects["data"]:
		print(i["id"], end = '\t', file = output_one)
		print(i["name_long"], end = '\t', file = output_one)


		string = str(ix_nets[str(i["id"])])
		string = string.replace('{\'"data": ','').replace(']"}','').replace('{"[','')
		string = string.replace('\'','')
		string = string.split(',')
		string = list(set(string))
		print(len(string), end = '\n',file = output_one)


def analysis_zero():
	
	'''Responsavel por realizar e imprimir em arquivo a analise zero 
		@names: dict
		@string: string
		@string: list
	'''

	output_zero = open('analise_zero.tsv','w')

	names = {}
	count_ixp = 0

	for i in net_names:
		names[i] = str(net_names[i])
		names[i] = names[i].replace('{\'"data":','').replace('}','')
		names[i] = names[i].replace('\'','')
		print(i , end= '\t', file = output_zero)	
		print(names[i], end= '\t', file = output_zero )

		for k in ix_objects["data"]:
			string = str(ix_nets[str(k["id"])])
			string = string.replace('{\'"data": ','').replace(']"}','').replace('{"[','')
			string = string.replace('\'','')
			string = string.replace(' ','')
			string = string.split(',')
			string = list(set(string))
			if str(i) in string:
				count_ixp = count_ixp + 1
		print(count_ixp, file = output_zero )
		count_ixp = 0


def main():
	entry_file = sys.argv[1]
	if  len(sys.argv) == 3:
		opt = int(sys.argv[2])
	else:
		print('err[0] escolha a analise 1 ou 2')
		return

	entry = entry_file.split(':')
	ip = entry[0]
	port = int(entry[1])

	handle_data(entry_file,ip,port)

	if opt == 1:
		analysis_one()
	elif opt == 0:	
		analysis_zero()
		

if __name__ == '__main__':
	main()






