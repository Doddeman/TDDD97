import sqlite3
from flask import g
import md5
DATABASE = 'database.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	get_db().commit()
	cur.close()
	return (rv[0] if rv else None) if one else rv

def validate_credentials(email, password, token):
	if token:
		res = query_db("SELECT email FROM online_users\
		WHERE token = ?", [token], True)
	else:
		#password = hash(password)
		password = md5.new(password).hexdigest()
		res = query_db("SELECT email FROM users\
		WHERE email = ? AND password = ?", [email, password], True)
	if res:
		return True
	return False

def get_hash_token(key, hashToken, saltList):
	token = query_db("SELECT token FROM online_users WHERE email = (?)", [key], True)[0]
	#print "got token: "
	#print token
	salt = ""
	for arg in saltList:
		salt += arg

	print "salt: "
	print salt

	hashSalt = token + salt

	print "hashSalt: "
	print hashSalt

	newHashToken = md5.new(hashSalt).hexdigest()
	#print "calulated token: "
	#print newHashToken
	#newHashToken = hash(hashSalt)
	if hashToken == newHashToken:
		print "MATCH"
		return True
	else:
		print "NOT MATCH"
		return False

def create_user(user):
	if len(query_db("SELECT email FROM users WHERE email = (?)", [user['email']])) > 0:
		return "Email already taken"

	#user['password'] = hash(user['password'])
	user['password'] = md5.new(user['password']).hexdigest()

	return query_db("INSERT INTO users VALUES (?,?,?,?,?,?,?)",\
	[user['email'], user['firstname'], user['familyname'],\
	user['gender'], user['city'], user['country'], user['password']])

def logout_other(email):
	token = query_db("SELECT token FROM online_users WHERE email = (?)", [email], True)
	if token:
		query_db("DELETE FROM online_users WHERE email is ?", [email])
		return ". Deleted old login"
		#return token

def add_user(email, token):
	query_db("INSERT INTO online_users VALUES (?,?)", [email, token])

def remove_user(email):
	try:
		query_db("DELETE FROM online_users WHERE email is ?", [email])
		return True
	except:
		#never fails, WHY??
		return False

def change_password(email, newPassword):
	#newPassword = hash(newPassword)
	newPassword = md5.new(newPassword).hexdigest()
	query_db("UPDATE users SET password = ? WHERE email = ?", [newPassword, email])

def find_user(token, user_email):
	if user_email: #find other user
		db_email = query_db("SELECT email FROM users WHERE email = (?)", [user_email])
		if db_email:
			target_email = db_email[0][0]
		else:
			return ""
	else: #find yourself
		own_email = query_db("SELECT email FROM online_users WHERE token = (?)", [token])
		target_email = own_email[0][0]

	data = query_db("SELECT email, firstname, familyname, gender,\
	city, country FROM users WHERE email = (?)", [target_email])

	user = {'email': data[0][0], 'firstname': data[0][1],\
	'familyname': data[0][2], 'gender': data[0][3],\
	'city': data[0][4], 'country': data[0][5]}
	return user


def get_messages(token, user_email):
	if user_email:
		db_email = query_db("SELECT email FROM users WHERE email = (?)", [user_email])
		if db_email:
			target_email = db_email[0][0]
		else:
			return False
	else:
		target_email = find_user(token, None)["email"] #get our own email with token

	all_messages = query_db("SELECT sender, content FROM messages WHERE\
	receiver = (?)", [target_email])
	result_msg = []
	for row in all_messages:
		sender = row[0]
		message = row[1]
		result_msg.append(sender)
		result_msg.append(message)
	return result_msg


def add_message(sender, message, receiver):
	#sender = query_db("SELECT email FROM online_users WHERE token = (?)", [token])[0][0]
	db_receiver = query_db("SELECT email FROM users WHERE email = (?)", [receiver])
	if db_receiver:
		query_db("INSERT INTO messages (sender, receiver, content) VALUES (?,?,?)",\
		[sender, receiver, message])
		return True
	else:
		return False
