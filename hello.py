# -*- coding: utf-8 -*-

from flask import Flask
from flask import (request, render_template,
					redirect, url_for, json)

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def index(name='Alexander'):
	context = {'name':name}
	return render_template('index.html',**context)

@app.route('/add/<int:num1>/<int:num2>')
def add(num1,num2):
	context = {'num1':num1,'num2':num2}
	return render_template('add.html',**context)

@app.route('/save', methods=['GET'])
def save():
	dogname = request.args.get('name', 0, type=str) + '!!!'
	if dogname == '!!!':
		dogname = 'А где же имя?'
	return json.jsonify(name=dogname)

app.run(debug=True)
