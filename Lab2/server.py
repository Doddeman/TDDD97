from random import *
from flask import Flask, request, jsonify
import database_helper as db
app = Flask(__name__)

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
		'familyname': data['familyname'], 'gender': data['gender'], \
		'city': data['city'], 'country': data['country'],\
		'password': data['password']}
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
		alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		token = ""
		for i in range(0, 36):
			rand = randint(0, len(alphabet)-1)
			sign = alphabet[rand]
			token += sign
		db.add_user(data['email'], token)
		return jsonify({'success': True, 'message': 'Logged in successfully',\
		 'token': token})
	else:
		return jsonify({'success': False, 'message': 'Wrong username or password'})

@app.route('/signout', methods=['POST'])
def sign_out():
	data = request.get_json()
	expected = ["token"]
	missing = check_expected_json(expected, data)
	if len(missing) > 0:
		return jsonify({'success': False, 'message': 'Missing data',\
		'Missing data': missing})
	if db.remove_user(data['token']):
		return jsonify({'success': True, 'message': 'Logged out successfully'})
	else:
		return jsonify({'success': False, 'message': 'Could not log out'})

@app.route('/changepassword', methods=['POST'])
def change_password():
	data = request.get_json()
	expected = ["token", "old", "new"]
	missing = check_expected_json(expected, data)
	if len(missing) > 0:
		return jsonify({'success': False, 'message': 'Missing data',\
		'Missing data': missing})
	email = db.find_user(data['token'], None)["email"]
	if db.validate_credentials(email, data['old'], None):
		db.change_password(email, data['new'])
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
		return jsonify({'success': True, 'message': "Retrieved messages",\
		'data' : messages})
	else:
		return jsonify({'success': False, 'message': "Incorrect token"})

@app.route('/messagesemail/<token>/<email>', methods=['GET'])
def get_user_messages_by_email(token = None, email = None):
	result = db.get_messages(token, email)
	return result

@app.route('/post', methods=['POST'])
def post_message():
	data = request.get_json()
	expected = ["token", "message", "receiver"]
	missing = check_expected_json(expected, data)
	if len(missing) > 0:
		return jsonify({'success': False, 'message': 'Missing data',\
		'Missing data': missing})
	if db.validate_credentials(None, None, token):
		db.add_message(data['token'], data['message'], data['receiver'])
		return jsonify({'success': True, 'message': "Message posted"})

if __name__== "__main__":
	init_db()
	app.run(port = 8000, debug = True)
