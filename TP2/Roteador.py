import socket 
import json
import struct
import time

class Router():
	def __init__(self, ip, name, port, period ):
		self.ip = ip
		self.port = port
		self.name = name
		self.listAdj = {}	# vizinhos
		self.period = period


		#self.nodes = dv_Table()
		
	def initSocket(self):
		self.router = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.router.bind((self.ip,self.port))
	
	def addNeighbors(self, neighbor, cost):
		self.listAdj[neighbor] = cost

	def delNeighbors(self, neighbor):
		if neighbor in self.listAdj:
			self.listAdj.pop(neighbor)
		
	def Run(self):
		'''Iniciando thread para receber mensagem '''
		receive_t = threading.Thread(target = self.recv_Message)
		receive_t.daemon = True
		receive_t.start()

		'''	Iniciando thread para enviar mensagem'''
		send_t = threading.Thread(target = self.send_Message)
		send_t.daemon = True
		send_t.start()

		''' Iniciando thread para remover rotas invalidas'''
		remove_t = threading.Thread(target = self.remove_Message)
		remove_t.daemon = True
		remove_t.start()

	
	def send_update():
		pass


	def send_Message(self, destination):
		while True:
			time.sleep(self.period)
			self.send_update()

		
	def recv_Message():
		while True:		
			msg, ip = self.router(recvfrom(2048))
			msg = json.loads(msg.decode('ascii'))

			if msg['type'] == update:
				pass #h_update()
			if msg['type'] == trace:
				pass #h_trace()
			if msg['type'] == data
				pass #h_data()


	def remove_Message():
		pass

	def add_link(self, cost, neighbor):
		self.addNeighbors(cost, neighbor)
		
	def del_link(self, neighbor):
		self.delNeighbors(neighbor)
		

	def send_Message(self, source, destination, hops):
		pass

	def h_trace(self, msg):
		
		if msg['destination'] != self.ip:
			msg['hops'].append(self.ip)
			#encaminha trace
		else: 
			payload = json.dumps(msg)
			new_msg = msg_data(self.ip, msg['source'], payload)
			#encaminha thread para destino

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


class dv_Table():
	def __init__(self):
		self.table = {}



class parser_Inputfile():
	def __init__(self, file, router):
		self.input = file				
		self.router = router
	def parse(self):		
		f = open(self.input, 'r')
		text = f.readlines()
		for line in text:
			lineList = line.split()
			print(lineList)
			if lineList[0] == 'add':
				self.router.add_link(lineList[1],lineList[2])
			elif lineList[0] == 'del':
				self.router.del_link(lineList[1])
			elif lineList[0] == 'trace':
				self.router.trace(lineList[1])


R1 = Router('127.0.0.1','A',5151)
R2 = Router('127.0.0.2','B',5151)
R3 = Router('127.0.0.3','C',5151)
R4 = Router('127.0.0.4','D',5151)
R5 = Router('127.0.0.5','E',5151)
R6 = Router('127.0.0.6','F',5151)


R1.initSocket()

P1 = parser_Inputfile("entrada.txt",R1)
P1.parse()

print('\n')




