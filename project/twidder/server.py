from random import randint
from flask import Flask, request, jsonify, json
from flask_sockets import Sockets
from gevent.wsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket import WebSocketError
import database_helper as db

app = Flask(__name__, static_url_path='')
socket = Sockets(app)

socket_connections = {}

@app.route('/')
def root():
	return app.send_static_file(filename='client.html')

def init_db():
	with app.app_context():
		database = db.get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			#if db is None:
			database.cursor().executescript(f.read())
		database.commit()

@app.teardown_appcontext
def close_connection(exception):
	db.close_db()

@socket.route('/echo')
def echo_socket(ws):
	while True:
		email = ws.receive()
		socket_connections[email] = ws
		#for k, v in socket_connections.items():
		#	print(k,v)
#return

def check_expected_json(exp, data):
	missing = []
	for key in exp:
		try:
			if not len(data[key]) > 0:
				missing.append(key)
		except:
			missing.append(key)
	return missing

@app.route('/signup', methods=['POST'])
def sign_up():
	data = request.get_json()
	expected = ["email", 'firstname', 'familyname', 'gender',\
	'city', 'country', "password"]
	missing = check_expected_json(expected, data)
	if len(missing) > 0:
		return jsonify({'success': False, 'message': 'Missing data',\
		'Missing data': missing})

	if len(data['password']) >= 6:
		user = {'email': data['email'], 'firstname': data['firstname'],\
		'familyname': data['familyname'], 'gender': data['gender'],\
		'city': data['city'], 'country': data['country'],\
		'password': data['password']};
		msg = db.create_user(user)
		if isinstance(msg, str):
			return jsonify({'success': False, 'message': msg})
		return jsonify({'success': True, 'message': "User successfully created"})
		#fixa check for om email redan existerar
		#else:
		#	return jsonify({'success': False, 'message': "Could not create user"})
	else:
		return jsonify({'success': False, 'message': 'Password too short'})

@app.route('/signin', methods=['POST'])
def sign_in():
	data = request.get_json()
	expected = ["email", "password"]
	missing = check_expected_json(expected, data)
	if len(missing) > 0:
		return jsonify({'success': False, 'message': 'Missing data',\
		'Missing data': missing})
	if db.validate_credentials(data['email'], data['password'], None):
		#Logout from other browser
		logout_msg = db.logout_other(data['email'])
		if data['email'] in socket_connections:
			ws = socket_connections[data['email']]
			ws.send("signout")
			#ws.send(json.dumps({"data": "sign_out"}))
			ws.close() #creates error
			del socket_connections[data['email']]

		#create token
		alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		token = ""
		for i in range(0, 36):
			rand = randint(0, len(alphabet)-1)
			sign = alphabet[rand]
			token += sign
		db.add_user(data['email'], token)

		success_msg = 'Logged in successfully'
		if isinstance(logout_msg, str):
			success_msg += logout_msg
		return jsonify({'success': True, 'message': success_msg, 'token': token})
	else:
		return jsonify({'success': False, 'message': 'Wrong username or password'})

@app.route('/signout', methods=['POST'])
def sign_out():
	data = request.get_json()
	expected = ["hashToken", "key", "salt"]
	missing = check_expected_json(expected, data)
	if len(missing) > 0:
		return jsonify({'success': False, 'message': 'Missing data',\
		'Missing data': missing})

	#check md5-token
	args = [data['salt']]
	if not db.get_hash_token(data['key'], data['hashToken'], args):
		return jsonify({'success': False, 'message': "Incorrect token"})

	if db.remove_user(data['key']):
		return jsonify({'success': True, 'message': 'Logged out successfully'})
	else:
		return jsonify({'success': False, 'message': 'Could not log out'})

@app.route('/changepassword', methods=['POST'])
def change_password():
	data = request.get_json()
	#revershash token
	expected = ["hashToken", "old", "new", "key"]
	missing = check_expected_json(expected, data)
	if len(missing) > 0:
		return jsonify({'success': False, 'message': 'Missing data',\
		'Missing data': missing})

	#check md5-token
	args = [data['old'], data['new']]
	if not db.get_hash_token(data['key'], data['hashToken'], args):
		return jsonify({'success': False, 'message': "Incorrect token"})

	#email = db.find_user(data['token'], None)["email"] #Still needed?
	if db.validate_credentials(data['key'], data['old'], None):
		db.change_password(data['key'], data['new'])
		return jsonify({'success': True, 'message': "Successfully changed password"})
	else:
		return jsonify({'success': False, 'message': "Old password incorrect"})

@app.route('/findself', methods=['GET'])
def get_user_data_by_token(token = None):
	token = request.headers.get("Authorization")
	user = db.find_user(token, None)
	if user:
		return jsonify({'success': True, 'message': "Found user info", "data": user})
	else:
		return jsonify({'success': False, 'message': "No such user"})

@app.route('/findother/<email>', methods=['GET'])
def get_user_data_by_email(token = None, email = None):
	token = request.headers.get("Authorization")
	if db.validate_credentials(None, None, token):
		user = db.find_user(token, email)
		if isinstance(user, dict):
			return jsonify({'success': True, 'message': "Found user info", "data": user})
		else:
			return jsonify({'success': False, 'message': "No such user"})
	else:
		return jsonify({'success': False, 'message': "Incorrect token"})

@app.route('/messagestoken', methods=['GET'])
def get_user_messages_by_token(token = None):
	token = request.headers.get("Authorization")
	if db.validate_credentials(None, None, token):
		messages = db.get_messages(token, None)
		return jsonify({'success': True, 'message': "Retrieved user's messages",\
		'data' : messages})
	else:
		return jsonify({'success': False, 'message': "Incorrect token"})

@app.route('/messagesemail/<email>', methods=['GET'])
def get_user_messages_by_email(token = None, email = None):
	token = request.headers.get("Authorization")
	if db.validate_credentials(None, None, token):
		messages = db.get_messages(token, email)
		if isinstance(messages, list):
			return jsonify({'success': True, 'message': "Retrieved other user's messages",\
		'data' : messages})
		else:
			return jsonify({'success': False, 'message': "No such user"})
	else:
		return jsonify({'success': False, 'message': "Incorrect token"})

@app.route('/post', methods=['POST'])
def post_message():
	data = request.get_json()
	expected = ["hashToken", "message", "receiver", "key"]
	missing = check_expected_json(expected, data)
	if len(missing) > 0:
		return jsonify({'success': False, 'message': 'Missing data',\
		'Missing data': missing})

	#check md5-token
	args = [data['message'], data['receiver']]
	if not db.get_hash_token(data['key'], data['hashToken'], args):
		return jsonify({'success': False, 'message': "Incorrect token"})


	success = db.add_message(data['key'], data['message'], data['receiver'])
	if success:
		print "success"
		return jsonify({'success': True, 'message': "Message posted"})
	else:
		print "receiver not found"
		return jsonify({'success': False, 'message': "Receiver not found"})

if __name__== "__main__":
	print "starting server"
	init_db()
	app.debug = True
	#app.run(port = 8000, debug = True)
	http_server = WSGIServer(('', 8000), app, handler_class=WebSocketHandler)

	http_server.serve_forever()
