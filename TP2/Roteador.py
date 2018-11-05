#!/usr/bin/env python3


import socket 
import json
import struct
import time
import threading
import numpy as np
import random
import sys

table_lock = threading.Lock() #Lock de acesso da tabela de rotemaneto 
valid_lock = threading.Lock() #Lock de acesso a lista de rotas válidas

class Router():
	def __init__(self, ip, port, period ):
		''' 
			@ip: String
			@port: int
			@listAdj: dict - dicionario que contém os vizinhos imediatos do roteador
			@listValid: dict - dicionario que contém a lista de vizinhos validos (qu ainda estão conectados)
			@period: int - tempo determinado para o update de rotas
			@table: obj - tabela de roteamento   
		'''
		self.ip = ip
		self.port = port
		self.listAdj = {}	# vizinhos
		self.listValid = {} #vizinhos
		self.period = period
		self.table = dv_Table()
		
	def initSocket(self):
		self.router = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.router.bind((self.ip,self.port))
	
	def addNeighbors(self, neighbor, cost):
		''' Adiciona vizinhos imediatos'''
		self.listAdj[neighbor] = cost

	def delNeighbors(self, neighbor):
		'''Remove vizinhos imediatos '''
		if neighbor in self.listAdj:
			self.listAdj.pop(neighbor)
		
	def Run(self):
		''' Iniciando thread para remover rotas invalidas'''
		remove_t = threading.Thread(target = self.remove_invalid_routes)
		remove_t.daemon = True
		remove_t.start()

		'''Iniciando thread para receber mensagem '''
		receive_t = threading.Thread(target = self.recv_Message)
		receive_t.daemon = True
		receive_t.start()

		'''	Iniciando thread para enviar mensagem'''
		send_t = threading.Thread(target = self.send_message_update)
		send_t.daemon = True
		send_t.start()
	'''----------------------------------------------------------------------------------- '''	

	'''----------------------------------------------------------------------------------- '''
	def send_message_update(self):
		while True:
			time.sleep(self.period)
			self.send_update()
			
	def recv_Message(self):
		'''Recebe a mensagem e trata de acordo com seu tipos '''
		while True:		
			msg, ip = self.router.recvfrom(2048)
			msg = json.loads(msg.decode('ascii'))

			if msg['type'] == 'update':
				self.h_update(msg)
			if msg['type'] == 'trace':
				self.h_trace(msg)
			if msg['type'] == 'data':
				self.h_data(msg)
		
	def remove_invalid_routes(self):
		'''Responsável por remover as rotas que já não estão ativas da tabela de roteamento '''
		while True:
			invalid = []
			time.sleep(self.period)
			for i in self.listValid:
				if self.listValid[i] == 4:
					invalid.append(i)
			for d in invalid:
				if d in self.listValid:
					valid_lock.acquire()
					del self.listValid[d]
					valid_lock.release()
					self.table.remove_table(d)
			valid_lock.acquire()
			for i in self.listValid:
				self.listValid[i] = self.listValid[i] + 1
			valid_lock.release()	
			
	'''--------------------------------------------------------------------------------- '''

	'''--------------------------------------------------------------------------------- '''
	def up_valid(self, neighbor):
		''' Renova as rotas invalidas, setando o valor do 'ttl' para 0 '''
		valid_lock.acquire()
		self.listValid[neighbor] = 0
		valid_lock.release()

	def del_valid(self, neighbor):
		'''deleta o vizinho que não fornece uma rota valida '''
		del self.listValid[neighbor]

	def add_valid(self, neighbor):
		'''Adiciona uma rota valida '''
		self.listValid[neighbor] = 0

	def add_link(self, cost, neighbor):
		'''Adiciona link entre dois roteadores '''
		self.addNeighbors(cost, neighbor)
	
	def del_link(self, neighbor):
		'''deleta link entre dois roteadores '''
		self.delNeighbors(neighbor)
	'''-----------------------------------------------------------------------------------'''

	'''---------------------------------------------------------------------------------- '''	
	def trace(self,destination):
		'''Envia a msg de traceroute '''
		msg = self.msg_trace(self.ip,destination,self.table.table)
		list_next_hops = self.table.distance_vector_algorithm()
		if destination in list_next_hops:
			self.send_Message(msg,list_next_hops[destination])
	
	def send_update(self):
		'''Envia a tabela de rotas para roteadores vizinhos '''
		for i in self.listAdj:
			msg = self.msg_update(self.ip, i, self.table.table)			
			self.router.sendto(msg, (i,self.port))

	def send_Message(self, msg,  next_hop):
		'''envia a mensagem para o próximo destino de acordo com a tabela de roteamento '''
		self.router.sendto(msg,(next_hop, self.port))
	'''---------------------------------------------------------------------------------- '''
	
	'''---------------------------------------------------------------------------------- '''

	def h_trace(self, msg):
		'''Trata a mensagem de trace, caso seja o destino ele envia novamente a msg para fonte como data.Caso contrário ele adiciona 
		a seu ip e encaminha a msg '''

		'''
			@list_next_hops: dict - lista que recebe os hops para onde a msg será encaminhada
		'''

		list_next_hops = self.table.distance_vector_algorithm()
		if msg['destination'] != self.ip:
			msg['hops'].append(self.ip)
			if msg['destination'] in list_next_hops:
				n = msg['destination']
				self.send_Message(msg,list_next_hops[n])
		else: 
			payload = json.dumps(msg)
			new_msg = self.msg_data(self.ip, msg['source'], payload)
			n = msg['source']
			self.send_Message(new_msg, list_next_hops[n])

	def h_data(self,msg):
		'''Trata a msg de dados,caso self.ip for o destino a função imprime o payload caso contrario encaminha a msg '''

		if msg['destination'] == self.ip:
			payload = json.dumps(msg)
			print(payload)
		else:
			list_next_hops = self.table.distance_vector_algorithm()
			if msg['destination'] in list_next_hops:
				n = msg['destination']
				self.send_Message(msg, list_next_hops[n])

	def h_update(self,msg):
		'''Trata as mensagens de update, adiciona as rotas inexistentes na tabela de roteamento e atualiza as rotas '''
		for destination in msg['distances']:
			for next_hop in msg['distances'][destination]:
				if next_hop != self.ip and destination != self.ip:
					cost = int(msg['distances'][destination][next_hop]) + int(self.get_costs(msg['source']))
					self.table.add_table(destination,msg['source'],cost)
					self.up_valid(msg['source'])

		
	def get_costs(self, source): 
		''' Retorna o custo de determinado enlace do roteador com um determinado vizinho '''
		cost = self.listAdj[source]
		return cost

	'''-----------------------------------------------------------------------------------'''
 
	'''------------------------------------------------------------------------------------'''
	'''Funções de construção das mensagens '''
	def msg_update(self, source, destination, distances):
		msg = {
			"type": "update",
			"source": source,
			"destination": destination,
			"distances": distances
		}

		return json.dumps(msg).encode('ascii')
	
	def msg_trace(self, source, destination, hops):
		msg = {
			"type": "trace",
			"source": source,
			"destination": destination,
			"hops": hops

		}

		return json.dumps(msg).encode('ascii')

	def msg_data(self, source, destination, payload):
		msg = {
			"type" : "data",
			"source" : source,
			"destination" : destination,
			"payload" : payload
		}

		return json.dumps(msg).encode('ascii')

	'''------------------------------------------------------------------------------------- '''	

class dv_Table():
	def __init__(self):
		self.table = {}
	
	'''------------------------------------------------------------------------------------- '''
	
	def add_table(self,destination, next_hop,cost):
		'''Adciona entrada na tabela de roteamento '''
		table_lock.acquire()
		if destination not in self.table:
			self.table[destination] = {}
		 
		self.table[destination][next_hop] = cost	#encontrar outra forma de adicionar o ttl
		table_lock.release()

	def remove_table(self,next_hop):
		'''Remove todas as entradas que possuiem o próximo salto = next_hop, ou seja, as rotas que não estão mais válidas '''
		table_lock.acquire()
		del_list = []
		for v,d in list(self.table.items()):
			for i in list(d.items()):
				if next_hop == i[0]:
					del self.table[v][i[0]]

			if(len(self.table[v]) == 0):
				del(self.table[v])


		#del(self.table[destination][next_hop])	#RESOLVER PROBLEMA DA TABELA !!!!!!!!!!

		
		table_lock.release()
	'''------------------------------------------------------------------------------------- '''		

	'''------------------------------------------------------------------------------------- '''
	def distance_vector_algorithm(self):
		'''Trecho de código que faz o processo de identificação de menor rota para cada destino '''

		next_hop = {}
		for v,d in list(self.table.items()):
			min_cost = 2**30
			for i in list(d.items()):
				if float(i[1]) < min_cost:
					min_nexthop = i[0]
					min_cost = float((i[1]))
					destination = v
		
			next_hop[destination] = min_nexthop
		return next_hop			
			
	
	'''------------------------------------------------------------------------------------- '''


class parser_Inputfile():
	def __init__(self, file, router):
		self.input = file				
		self.router = router
	def parse(self):		
		f = open(self.input, 'r')
		text = f.readlines()
		for line in text:
			lineList = line.split()
			if lineList[0] == 'add':
				self.router.add_link(lineList[1],lineList[2])

				self.router.table.add_table(lineList[1],lineList[1],lineList[2])	#introdução dos vizinhos na tabela de roteamento
			elif lineList[0] == 'del':
				self.router.del_link(lineList[1])
			elif lineList[0] == 'trace':
				self.router.trace(lineList[1])
			else:
				print('--error--')	
			

def main():
	count = len(sys.argv)
	R = Router(sys.argv[1],55151,3)
	R.initSocket()
	P = parser_Inputfile(str(sys.argv[2]),R)
	P.parse()
	R.Run()
	time.sleep(100)
	print("tabela 1-----------------")
	print(R.table.table)

main()
'''
R1 = Router('127.0.0.1','A',5151,5)
R2 = Router('127.0.0.2','B',5151,5)
R3 = Router('127.0.0.3','C',5151,5)
R4 = Router('127.0.0.4','D',5151,5)
R5 = Router('127.0.0.5','E',5151,5)
R6 = Router('127.0.0.6','F',5151,5)

R1.initSocket()
R2.initSocket()
R3.initSocket()
R4.initSocket()
R5.initSocket()
R6.initSocket()

P1 = parser_Inputfile("entrada.txt",R1)
P1.parse()
P2 = parser_Inputfile("entrada2.txt",R2)
P2.parse()
P3 = parser_Inputfile("entrada3.txt",R3)
P3.parse()
P4 = parser_Inputfile("entrada4.txt", R4)
P4.parse()
P5 = parser_Inputfile("entrada5.txt",R5) 
P5.parse()
P6 = parser_Inputfile("entrada6.txt",R6)
P6.parse()


R1.Run()
R2.Run()
R3.Run()
R4.Run()
R5.Run()
R6.Run()

time.sleep(15)
'''



'''
print("\ntabela 2-----------------")
print(R2.table.table)

print("\ntabela 3-----------------")
print(R3.table.table)

print("\ntabela 4------------------")
print(R4.table.table)

print("\ntable 5-------------------")
print(R5.table.table)

print("\ntable 6 ------------------")
print(R6.table.table)
'''



