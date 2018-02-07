import sqlite3
from flask import g
DATABASE = 'database.db'



def init_db(app):
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		connection = sqlite3.connect(DATABASE)
		c = connection.cursor()



		# Insert a row of data
		c.execute("INSERT INTO users VALUES (NULL, 'test@test', 'David', 'Wajngot', 'male', 'linkan', 'Sweden', '123123')")


		# Save (commit) the changes
		connection.commit()

		# We can also close the connection if we are done with it.
		# Just be sure any changes have been committed or they will be lost.
		connection.close()
	return db
