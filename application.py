import os

from flask import Flask
from sqlalchemy import create_engine
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from flask_login import LoginManager, login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DEBUG'] = True
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))
db = SQLAlchemy(app)


#recaptcha = GoogleReCaptcha(app)

login = LoginManager(app)
login.login_view = 'index'


import routes, models

if __name__ == "__main__":
	app.run(routes, debug=True)