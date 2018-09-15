#-*-coding:utf-8-*-
import sys
import socket
import select
import time
import math
import hashlib
from optparse import OptionParser
from threading import Thread
from threading import Condition
from random import randint
				
class Buffer:
	def __init__(self,tam):
		self.buffer = [None for i in range(tam)]
		self.tamBuffer = tam
		self.tamanhoAtual = 0
	def atualizarTam(self): #atualizar tamanho do buffer
		return self.tamBuffer - self.buffer.count(None)
	def inserirBuffer(self,elem): #Toda vez que o programa receber o ack do primeiro elemento do buffer, a janela irá andar.
		self.buffer.pop(0)
		self.buffer.append(elem)
		self.tamanhoAtual = self.atualizarTam()
	def retirarBuffer(self):
		self.buffer.pop(0)
		self.buffer.append(None)
		self.tamanhoAtual = self.atualizarTam()
	def liberarBuffer(self):
		self.buffer = [None for i in range(self.tamBuffer)]
		self.tamanhoAtual = 0
	
class Conexao:
	def __init__(self,ip,porta,ipServ):
		self.ip = ip
		self.porto = porta
		self.ipServ = ipServ
	def iniciaSock(self):
		self.sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) #inicia o socket para transferencia de dados via UDP
		return self.sock 	

	def leituraArq(self):
		arq = open("text.txt","r") #
		msg = arq.readline()
		return msg 


class somaVerif:
	def __init__(self,msgSender,msgReceiver):
		self.msgS = msgSender 
		self.msgR = msgReceiver
	def hash(self): 	
		self.hash = hashlib.md5(self.msgD.encode())
		return self.hash
	def hashQ(self):
		self.msgQ = 'erro'+self.msgSender 
		self.hash = hashlib.md5(self.msgQ.encode())
		return self.hash
	def verif(self,hash1,hash2):
		if hash1.digest() == hash2.digest():
			return True
		else:
			return False

class packetHandler:
	



'''teste'''
connection = Conexao("127.0.0.1",5152,"127.0.0.1")
sock = connection.iniciaSock()
msg = connection.leituraArq()

#while True:
c = sock.sendto(msg.encode(),(connection.ipServ,connection.porto))
msg = connection.leituraArq()

ha = somaVerif(msg)
hg = somaVerif(msg)
num = ha.hash()
num2 = hg.hashQ()
if num.digest() == num2.digest():
	print("Everything is fine\n")
else:
	print("i'm screwed\n")
print(num.digest())

sock.close()

'''class somaVerif:
	def __init__(self,msg):
		self.msgD = msg
	def hash(self):	
		self.hash = hashlib.md5(self.msgD.encode())
		return self.hash
	def hashQ(self):
		self.msgQ = 'erro'+self.msgD 
		print(self.msgQ)
		self.hash = hashlib.md5(self.msgQ.encode())
		return self.hash
'''