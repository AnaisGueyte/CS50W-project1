
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from wtforms import Form, StringField, SubmitField, PasswordField, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
from application import app, db
from models import *

from flask_login import login_required, login_user, login_manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, func, and_, or_

import requests
import json
import re
import random
import pickle

#cors = CORS(app, resources={r"/api/*": {"origins": "http://motsmagiques.fr/, https://motsmagiques.fr/"}})

####################### FRONT #######################

class MyForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():

    form = MyForm(request.form)

    if request.method == 'POST' and form.validate():
        user = Auth_user()
        user = Auth_user.query.filter_by(username=form.username.data).first()

        if user:
            is_password_true = check_password_hash(user.password, form.password.data)

        if user is None:
            flash('Oh, oh! This user isn\'t registered', 'alert alert-danger')
            return redirect(url_for('index'))

        if is_password_true is False:
            login_user(user)
            return redirect(url_for('dashboard'))

        else:
            login_user(user)
            return redirect(url_for('dashboard'))
    else:
        return render_template('home.html', form=form)

    return render_template('home.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = MyForm(request.form)

    if request.method == 'POST' and form.validate():

        user = Auth_user()
        user.username = form.username.data
        password = form.password.data
        user.password = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()

        flash("Account successfully created", 'alert alert-success')
        return redirect(url_for("dashboard"))

    return render_template('home.html', form=form)

    
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "xBKc2kBrb6SrUUxzmEvXQ", "isbns": "9781632168146"})
    #print(res.json())

    return render_template('dashboard.html')