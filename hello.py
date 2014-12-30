# -*- coding: utf-8 -*-
import sqlite3 as lite
from flask import Flask
from flask import (request, render_template,
					redirect, url_for, json)

app = Flask(__name__)

# SqlAlchemy

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:22061945@localhost:5432/flaskdb')

from sqlalchemy import Table, Column, Integer, String, Text, Boolean, MetaData, ForeignKey


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Message(Base):
	__tablename__ = 'messages'
	id = Column(Integer, primary_key=True)
	user = Column(String)
	text = Column(Text)
	read = Column(Boolean)
 
	def __init__(self, user, text, read):
		self.user = user
		self.text = text
		self.read = read
	def __repr__(self):
		return "User:%s'\nMessage:'%s'\nRead:'%s'"%(self.user, self.text, self.read)
	def serialize(self):
		return [{'user': self.user, 'text':self.text}]

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
@app.route('/<name>')
def index(name='Alexander'):
	context = {'name':name}
	return render_template('index.html',**context)

@app.route('/add/<int:num1>/<int:num2>')
def add(num1,num2):
	context = {'num1':num1,'num2':num2}
	return render_template('add.html',**context)

@app.route('/send', methods=['POST'])
def send():
	user = request.form['user']
	text = request.form['text']
	if text:
		message = Message(user,text,False)
		session.add(message)
		session.commit()
		print json.jsonify(text=text)
	return json.jsonify(text=text)

@app.route('/update', methods=['GET'])
def update():
	user = request.args.get('user')
	if user:
		post = []
		messages = session.query(Message).filter(Message.user!=user).filter(Message.read==False).all()
		for message in messages:
			post += message.serialize()
			message.read=True;
		# Save (commit) the changes
		session.commit()
	return json.jsonify(messages=post)

app.run(debug=True)
