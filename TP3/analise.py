#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import matplotlib.pyplot as plt
import numpy as np

global value 
const = 20

def count(int_array):

	count = []
	value = const

	equal_than_list = np.equal(int_array, 0)
	count.append(np.count_nonzero(equal_than_list))


	for i in range(0,int(200/const)):
		less_than_list = np.less(int_array, value)
		count.append(np.count_nonzero(less_than_list))
			
		value = value + const


	return count	

def get_data():

	dataset = open('analise_zero.tsv')
	int_list = []

	for line in dataset:
		string_value = line.strip()
		list_value = string_value.split('\t')
		int_list.append(list_value[2])
	
	int_list = list(map(int, int_list))

	int_array = np.asarray(int_list)	
	#print(np.amax(int_array))
	#print(np.amin(int_array))

	return int_array


def plot(Y):
	X = []
	k = 0
	for i in range(0,int(200/const) + 1):
		X.append(k)
		k = k + const
	
	p = plt.scatter(X,Y)
	plt.xticks(np.arange(min(X), max(X)+1, 20.0))	
	plt.title('IXP x Net')
	plt.xlabel('X - Variavel aleatoria(IXP)')
	plt.ylabel('F(X)')

	plt.show()


def main():
	int_array = get_data()
	c = count(int_array)
	
	Y = np.divide(c,len(int_array))
	plot(Y)



if __name__ == '__main__':
	main() 
