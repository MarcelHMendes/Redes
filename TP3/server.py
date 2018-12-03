#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, jsonify, request, render_template, url_for, request_finished


def loadData():
	global net_data
	global ix_data
	global nixlan_data
	
	PATH_net = os.path.realpath(os.path.dirname(__file__))
	json_path = os.path.join(PATH_net, "files", "net.json")
	net_data = json.load(open(json_path))

	PATH_ix = os.path.realpath(os.path.dirname(__file__))
	json_path = os.path.join(PATH_ix , "files", "ix.json")
	ix_data = json.load(open(json_path))

	PATH_nilan = os.path.realpath(os.path.dirname(__file__))
	json_path = os.path.join(PATH_nilan, "files", "netixlan.json")
	nixlan_data = json.load(open(json_path))

	#ler arquivos da linha de comando

app = Flask(__name__)

'''@app.route("/", methods = ['GET','POST'])
def hello():
	return 'Hello'
'''
@app.route('/api/ix')
def showjson_ix():
	return jsonify(ix_data)

@app.route('/api/ixnets/<ix_id>', methods= ['GET'])
def show_json(ix_id):
	net_list = []

	for i in nixlan_data['data']:
		if i['ix_id'] == int(ix_id):
			net_list.append(i['net_id'])  
			
	data = {"data":net_list}		
	return jsonify(data)

@app.route('/api/netname/<net_id>', methods= ['GET'])
def showjson_net(net_id):
	net_id = int(net_id) + 1
	log_response = 'End of file'
	try:
		data = {"data": net_data['data'][net_id]['name']}
		return jsonify(data)
	except:
		request_finished.connect(app)
	#verificar net id
if __name__ == '__main__':
	loadData()
	app.run(debug=True)