from flask import Flask, request, jsonify
from database_helper import *
app = Flask(__name__)

#@app.route("/")
#def hello():
#    return "Hello World, jdafbgka"

#def init_db(app):
#	with app.app_context():
#		db = get_db()
#		with app.open_resource('schema.sql', mode='r') as f:
#			if db is None:
#				db.cursor().executescript(f.read())
#		db.commit()

@app.route('/', methods=['POST'])
def sign_up():
	user_email = request.json['email']
	#Glom ej check for om user redan finns!
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
		for value in user.values():
			#user.get('Age')
			if len(value) < 1:
				return jsonify({'success': False, 'message': 'Empty variable'})
		add_user(user)
		return jsonify({'success': True, 'message': 'User successfully created'})
	else:
		return jsonify({'success': False, 'message': 'Password too short'})

@app.route('/signin', methods=['POST'])
def sign_in():
	user_email = request.json['email']
	password = request.json['password']

	if try_login(user_email, password):
		#token = "hejhej"
		return jsonify({'success': True, 'message': 'Logged in successfully'})
	else:
		return jsonify({'success': False, 'message': 'Wrong username or password'})




#if __name__== "__main__":
#    app.run(port = 8000, debug = True)
