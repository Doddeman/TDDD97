from flask import Flask, request, jsonify
from database_helper import *
app = Flask(__name__)

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			#if db is None:
			db.cursor().executescript(f.read())
		db.commit()

@app.route('/signup', methods=['POST'])
def sign_up():
	user_email = request.json['email']
	first_name = request.json['firstname']
	family_name = request.json['familyname']
	gender = request.json['gender']
	city = request.json['city']
	country = request.json['country']
	password = request.json['password']
	if len(password) >= 6:
		user = {'email': user_email, 'firstname': first_name,\
		'familyname': family_name, 'gender': gender, 'city': city,\
		'country': country, 'password': password}
		result = add_user(user)
		return result
	else:
		return jsonify({'success': False, 'message': 'Password too short'})

@app.route('/signin', methods=['POST'])
def sign_in():
	user_email = request.json['email']
	password = request.json['password']

	result = login(user_email, password)
		#token = "hejhej"
	return result

@app.route('/signout', methods=['POST'])
def sign_out():
	token = request.json['token']
	result = remove_user(token)
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
	result = db_find_user(token, None)
	return result

@app.route('/findother/<token>/<email>', methods=['GET'])
def get_user_data_by_email(token = None, email = None):
	result = db_find_user(token, email)
	return result

@app.route('/messagestoken/<token>', methods=['GET'])
def get_user_messages_by_token(token = None):
	result = db_get_messages(token)
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
