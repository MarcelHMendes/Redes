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


class Buffer():
	def __init__(self,tmax):
		self.buffer = [None for i in range(tam)]
		self.tamMax = tmax
		self.tam = 0

	def insereBuffer(self,elem):
		