#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, jsonify, request, render_template, url_for


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



app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])

def hello():
	if(request.method == 'POST'):
		some_json = request.get_json()
		return jsonify({'you sent': some_json}), 201
	else:	
		return jsonify({"about": "hello world"})
		

@app.route('/multi/<int:num>', methods= ['GET'])
def square(num):	
	result  = num * num
	return jsonify({'resultado': result})


@app.route('/user/<user_name>', methods= ['GET'])
def user(user_name):
	result = 'Hi!' + user_name
	return jsonify({'Reusltado': result})


@app.route('/file/ix')
def showjson_ix():
	return jsonify(ix_data)

@app.route('/file/net')
def showjson_net():
    return jsonify(net_data['data'][0]['name'])

@app.route('/file/nilan')
def show_json():
	return jsonify(nixlan_data)
	
if __name__ == '__main__':
	loadData()
	app.run(debug=True)

