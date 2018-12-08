#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import json
from flask import Flask, jsonify, request, render_template, url_for, request_finished
import logging

def loadData():
	global net_data
	global ix_data
	global nixlan_data
	
	#PATH_net = os.path.realpath(os.path.dirname(__file__))
	#json_path = os.path.join(PATH_net, "files", "net.json")
	json_path = sys.argv[1]
	net_data = json.load(open(json_path))

	#PATH_ix = os.path.realpath(os.path.dirname(__file__))
	#json_path = os.path.join(PATH_ix , "files", "ix.json")
	json_path = sys.argv[2]
	ix_data = json.load(open(json_path))

	#PATH_nilan = os.path.realpath(os.path.dirname(__file__))
	#json_path = os.path.join(PATH_nilan, "files", "netixlan.json")
	json_path = sys.argv[3]
	nixlan_data = json.load(open(json_path))

	#ler arquivos da linha de comando

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

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
	net_id = int(net_id) 
	log_response = 'End of file'
	
	if net_id < len(net_data['data']):	#testar limites
		data = {"data": net_data['data'][net_id]['name']}
		return jsonify(data)
	else:
		msg = '\nEOF\n'
		return msg
	#verificar net id
if __name__ == '__main__':
	loadData()
	app.run(debug=True)