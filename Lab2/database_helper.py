import sqlite3
from flask import g
DATABASE = 'database.db'



'''def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db'''

#connect = sqlite3.connect('database.db')
#c = connect.cursor()


def add_user(user):
	token = 'NULL'
	mail = user['email']
	firstname = user['firstname']
	familyname = user['familyname']
	gender = user['gender']
	city = user['city']
	country = user['country']
	password = user['password']

	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)",\
	[token, mail, firstname, familyname, gender, city, country, password])
	conn.commit()
	conn.close()

def find_user(user_email):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users WHERE email = (?)", [user_email])
	result = cursor.fetchall()
	for r in result:
	    print(r)

	conn.commit()
	conn.close()
	'''token = 'NULL'
	mail = user['email']
	firstname = user['firstname']
	familyname = user['familyname']
	gender = user['gender']
	city = user['city']
	country = user['country']
	password = user['password']'''

def try_login(email, password):
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	cursor.execute("SELECT password FROM users WHERE email = (?)", [email])
	data = cursor.fetchone()
	db_password = data[0]

	if len(db_password) >= 6 and db_password == password:
		token = "prutt"
		cursor.execute("UPDATE users SET token = ? WHERE email = ?", [token, email])
		conn.commit()
		conn.close()
		return True
	else:
		conn.commit()
		conn.close()
		return False




# Save (commit) the changes
#conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
#conn.close()
