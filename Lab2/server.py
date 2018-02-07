from flask import Flask
from database_helper import *
app = Flask(__name__)

#@app.route("/")
#def hello():
#    return "Hello World, jdafbgka"

if __name__== "__main__":
    init_db(app)
    app.run(port = 8000, debug = True)
