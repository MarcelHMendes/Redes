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

