import socket 
import json
import struct
import time
import threading
import numpy as np

table_lock = threading.Lock()

class Router():
	def __init__(self, ip, name, port, period ):
		self.ip = ip
		self.port = port
		self.name = name
		self.listAdj = {}	# vizinhos
		self.period = period
		self.table = dv_Table()
		
	def initSocket(self):
		self.router = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.router.bind((self.ip,self.port))
	
	def addNeighbors(self, neighbor, cost):
		self.listAdj[neighbor] = cost

	def delNeighbors(self, neighbor):
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
		pass
	'''--------------------------------------------------------------------------------- '''

	'''--------------------------------------------------------------------------------- '''
	def add_link(self, cost, neighbor):
		self.addNeighbors(cost, neighbor)
		
	def del_link(self, neighbor):
		self.delNeighbors(neighbor)
	'''-----------------------------------------------------------------------------------'''

	'''---------------------------------------------------------------------------------- '''	
	def trace(self,destination):
		msg = self.msg_trace(self.ip,destination)
		#encaminha_msg
	

	def send_update(self):
		for i in self.listAdj:
			msg = self.msg_update(self.ip, i, self.table.table)			
			self.router.sendto(msg, (i,self.port))

	def send_Message(self, msg,  next_hop):
		self.router.sendto(msg,(next_hop, self.port))
	'''---------------------------------------------------------------------------------- '''
	
	'''---------------------------------------------------------------------------------- '''

	def h_trace(self, msg):
		list_next_hops = self.table.distance_vector_algorithm()
		if msg['destination'] != self.ip:
			msg['hops'].append(self.ip)
			if msg['destination'] in list_next_hops:
				n = msg['destination']
				self.send_Message(msg,list_next_hops[n])
		else: 
			payload = json.dumps(msg)
			new_msg = msg_data(self.ip, msg['source'], payload)
			n = new_msg['destination']
			self.send_Message(new_msg, list_next_hops[n])

	def h_data(self,msg):
		if msg['destination'] == self.ip:
			payload = json.dumps(msg)
			print(payload)
		else:
			pass
			#encaminha msg

	def h_update(self,msg):
		for destination in msg['distances']:
			for next_hop in msg['distances'][destination]:
				if next_hop != self.ip and destination != self.ip:
					cost = int(msg['distances'][destination][next_hop]) + int(self.get_costs(msg['source']))
					self.table.add_table(destination,msg['source'],cost)
		#self.send_update()
		#encaminhar mensagem de update		
		#algoritmoVetorDistancia
		#h_update() resonsável por adicionar os custos cumulutivos

	def get_costs(self, source): 
		cost = self.listAdj[source]
		return cost

	'''-----------------------------------------------------------------------------------'''
 
	'''------------------------------------------------------------------------------------'''

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
		table_lock.acquire()
		if destination not in self.table:
			self.table[destination] = {}
		 
		self.table[destination][next_hop] = cost	#encontrar outra forma de adicionar o ttl
		table_lock.release()

	def remove_table(self,destination,next_hop):
		table_lock.acquire()
		del(self.table[destination][next_hop])	#RESOLVER PROBLEMA DA TABELA !!!!!!!!!!

		if(len(self.table[destination] == 0)):
			del(self.table[destination])
		table_lock.release()
	'''------------------------------------------------------------------------------------- '''		

	'''------------------------------------------------------------------------------------- '''
	def distance_vector_algorithm(self):
		next_hop = {}
		for v,d in list(self.table.items()):
			min_cost = 2**30
			for i in list(d.items()):
				if float(i[1]) < min_cost:
					min_nexthop = i[0]
					min_cost = float((i[1]))
					destination = v		

			next_hop[destination] = {min_nexthop}
		return next_hop		
			
	

	'''Por enquanto a mensagem de update não está sendo propagada indefinidamente por causa do comando break inserido 
	em send_update(), após a criação do distance_vector() a propagação irá parar quando não tiver nenhum update que diminua
	os custos de acesso na rede '''	





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

time.sleep(5)

#print(R1.table.distance_vector_algorithm())

print("tabela 1-----------------")
print(R1.table.table)

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




