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
	user_email = request.json['email']
	password = request.json['password']

	result = db_sign_in(user_email, password)
		#token = "hejhej"
	return result

@app.route('/signout', methods=['POST'])
def sign_out():
	token = request.json['token']
	result = db_sign_out(token)
	return result

@app.route('/changepassword', methods=['POST'])
def change_password():
	token = request.json['token']
	old_password = request.json['old']
	new_password = request.json['new']
	result = db_change_password(token, old_password, new_password)
	return result

@app.route('/findself/<token>', methods=['GET'])
def get_user_data_by_token(token = None):
	token = request.headers.get("Authorization")
	result = db_get_user_data(token, None)
	return result

@app.route('/findother/<token>/<email>', methods=['GET'])
def get_user_data_by_email(token = None, email = None):
	result = db_get_user_data(token, email)
	return result

@app.route('/messagestoken/<token>', methods=['GET'])
def get_user_messages_by_token(token = None):
	result = db_get_user_messages(token, None)
	return result

@app.route('/messagesemail/<token>/<email>', methods=['GET'])
def get_user_messages_by_email(token = None, email = None):
	result = db_get_user_messages(token, email)
	return result

@app.route('/post', methods=['POST'])
def post_message():
	token  = request.json['token']
	message = request.json['message']
	receiver_email = request.json['mail']
	result = db_post_message(token, message, receiver_email)
	return result

if __name__== "__main__":
	init_db()
	app.run(port = 8000, debug = True)
