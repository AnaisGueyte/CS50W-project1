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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fdlzfwsmgxqegf:2c83af2945a01c8021a131b59c7d0ce4b9aa73ced291373e77400b0bc3cf6db7@ec2-18-214-211-47.compute-1.amazonaws.com:5432/d6fbaqgtnl6083'


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

