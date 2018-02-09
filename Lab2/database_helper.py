import sqlite3
from flask import g, jsonify
from random import *
DATABASE = 'database.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

def add_user(user):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	try:  #if not email already taken
		token = None
		mail = user['email']
		firstname = user['firstname']
		familyname = user['familyname']
		gender = user['gender']
		city = user['city']
		country = user['country']
		password = user['password']

		cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)",\
		[token, mail, firstname, familyname, gender, city, country, password])
		conn.commit()
		conn.close()
		return jsonify({'success': True, 'message': 'User successfully created'})
	except Exception as error_message:
		conn.rollback()
		return jsonify({'success': False, 'message': str(error_message)})

def login(email, password):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT password FROM users WHERE email = (?)", [email])
		data = cursor.fetchone()
		db_password = data[0]
		if len(db_password) >= 6 and db_password == password:
			#Create token
			alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
			token = ""
			for i in range(0, 36):
				rand = randint(0, len(alphabet)-1)
				sign = alphabet[rand]
				token += sign
			cursor.execute("UPDATE users SET token = ? WHERE email = ?", [token, email])
			conn.commit()
			conn.close()
			return jsonify({'success': True, 'message': 'Logged in successfully',\
			 'token': token})
		else:
			conn.commit()
			conn.close()
			return jsonify({'success': False, 'message': 'Wrong username or password'})
	except Exception as error_message:
		conn.rollback()
		return jsonify({'success': False, 'message': str(error_message)})

def remove_user(token):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	#new_token = None
	try:
		cursor.execute("DELETE FROM users WHERE token is ?", [token])
		data = cursor.fetchone()
		db_password = data[0]
		conn.commit()
		conn.close()
		return jsonify({'success': True, 'message': 'Logged out successfully'})
	except Exception as error_message:
		#never fails, WHY??
		conn.rollback()
		return jsonify({'success': False, 'message': str(error_message)})

def db_change_password(token, old, new):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT password FROM users WHERE token = (?)", [token])
		data = cursor.fetchone()
		db_password = data[0]
		if db_password == old:
			try:
				cursor.execute("UPDATE users SET password = ? WHERE token = ?", [new, token])
				conn.commit()
				conn.close()
				return jsonify({'success': True, 'message': "successfully changed password"})
			except Exception as error_message:
				return jsonify({'success': False, 'message': str(error_message)})
		else:
			return jsonify({'success': False, 'message': "Old password incorrect"})
	except Exception as error_message:
		conn.rollback()
		return jsonify({'success': False, 'message': str(error_message)})

def db_find_user(token, user_email):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	try:
		if user_email: #find other user
			cursor.execute("SELECT token FROM users WHERE token = (?)", [token])
			data = cursor.fetchone()
			db_token = data[0]
			if db_token == token:
				cursor.execute("SELECT * FROM users WHERE email = (?)", [user_email])
			else:
				return jsonify({'success': True, 'message': "incorrect token"})
		else: #find yourself
			cursor.execute("SELECT * FROM users WHERE token = (?)", [token])

		result = cursor.fetchone()
		mail = result[1]
		firstname = result[2]
		familyname = result[3]
		gender = result[4]
		city = result[5]
		country = result[6]
		user = {'email': mail, 'firstname': firstname,\
		'familyname': familyname, 'gender': gender,\
		 'city': city, 'country': country}
		conn.commit()
		conn.close()
		return jsonify({'success': True, 'message': "Found user info", "data": user})
	except Exception as error_message:
		conn.rollback()
		return jsonify({'success': False, 'message': str(error_message)})

def db_get_messages(token):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	try: #see if token is correct
		cursor.execute("SELECT email FROM users WHERE token = (?)", [token])
		data = cursor.fetchone()
		sender_email = data[0] #will cast exception if email don't exist
	except Exception as error_message:
		conn.rollback()
		return jsonify({'success': False, 'message': str(error_message)})
	try:
		cursor.execute("SELECT content FROM messages WHERE receiver = (?)", [sender_email])
		result_msg = ""
		data = cursor.fetchall()

		for row in data:
			print row
			result_msg += data[row][1] + '\n' ##list indices must be whattt
		return jsonify({'success': True, 'message': "Retrieved messages", "data": result_msg})
	except Exception as error_message:
		conn.rollback()
		return jsonify({'success': False, 'message': str(error_message)})

def db_post_message(token, message, receiver_email):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	try: #see if token and receiver_email is correct
		cursor.execute("SELECT email FROM users WHERE token = (?)", [token])
		data = cursor.fetchone()
		sender_email = data[0] #will cast exception if email don't exist
		cursor.execute("SELECT email FROM users WHERE email = (?)", [receiver_email])
		data = cursor.fetchone()
		db_receiver_email = data[0] #will cast exception if email don't exist
	except Exception as error_message:
		return jsonify({'success': False, 'message': str(error_message)})
	try: #post message
		cursor.execute("INSERT INTO messages (sender, receiver, content) VALUES (?,?,?)",\
		[sender_email, receiver_email, message])
		conn.commit()
		conn.close()
		return jsonify({'success': True, 'message': "Message posted"})
	except Exception as error_message:
		return jsonify({'success': False, 'message': str(error_message)})
