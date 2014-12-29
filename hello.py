# -*- coding: utf-8 -*-
import sqlite3 as lite
from flask import Flask
from flask import (request, render_template,
					redirect, url_for, json)

app = Flask(__name__)

# Database configuration and helpers
DATABASE = 'tmp/chat.db'

con = lite.connect(DATABASE)
cur = con.cursor()

# cur.executescript("""
# 	drop table if exists messages;
# 	create table messages (
# 		id integer primary key autoincrement,
# 		author text not null,
# 		text text not null,
# 		read boolean not null
# 	);
#     """)
# cur.execute("INSERT INTO messages('author',text,read) VALUES('author','text',False);")
# con.commit()

# Create clean table
cur.execute('DROP TABLE IF EXISTS messages;')
cur.execute('''
	CREATE TABLE messages(
		id integer primary key autoincrement,
		user text not null,
		text text not null,
		read integer not null
	)''')

# Database end 


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
	print '\n ***NEW MESSAGE***'
	print user + ' <- user'
	print text + ' <- text \n'
	if text:
		
		con = lite.connect(DATABASE)
		cur = con.cursor()
		# Insert a row of data
		cur.execute("INSERT INTO messages(user,text,read) VALUES(?,?,0);",(user,text))
		# Save (commit) the changes
		con.commit()
	return json.jsonify(text=text)

@app.route('/update', methods=['GET'])
def update():
	user = request.args.get('user')
	if user:
		con = lite.connect(DATABASE)
		cur = con.cursor()
		# Insert a row of data
		# cur.execute('SELECT * FROM messages WHERE read=0 AND user <> ? ;', (user,))
		# messages = cur.fetchone()
		# print messages
		# messages = cur.fetchone()
		# print messages
		messages = []
		for message in cur.execute('SELECT * FROM messages WHERE read=0 AND user <> ? ;', (user,)):
			messages += [{'user':message[1],'text':message[2]}]
			cur.execute("UPDATE messages SET read = 1 WHERE id = ?",(message[0],))

		# Save (commit) the changes
		con.commit()
	return json.jsonify(messages=messages)

app.run(debug=True)
