
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from wtforms import Form, StringField, SubmitField, PasswordField, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
from application import app, db
from models import *
from routes_folder import search, review, book_page, api
from command import imports

from flask_login import login_required, login_user, login_manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, func, and_, or_

import requests
import json
import re
import random
import pickle



#search for books, leave reviews for individual books, and see the reviews made by other people

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
            flash('Oh, no! This user isn\'t registered', 'alert alert-danger')
            return redirect(url_for('index'))

        if is_password_true is False:
            flash('Oh, no! Something went wrong with the password, try again!', 'alert alert-danger')  
            return redirect(url_for('index'))

        if user and is_password_true is True:
            login_user(user)
            session['logged_in'] = True
            session['username'] = user.get_id()
            flash('Welcome!', 'alert alert-success')  
            return redirect(url_for('search'))

        else:
            flash('Wow! Something went wrong, try again?', 'alert alert-danger')  
            return redirect(url_for('index'))

    return render_template('home.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = MyForm(request.form)

    if request.method == 'POST' and form.validate():

        user = Auth_user()
        user.username = form.username.data

        username_exist = Auth_user.query.filter(Auth_user.username == user.username).first()

        if username_exist is None:

            password = form.password.data
            user.password = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()

            session['logged_in'] = True
            session['username'] = user.get_id()

            flash("Account successfully created, Welcome!", 'alert alert-success')
            return redirect(url_for("search"))

        else:
            flash("Oh, no! This user already exists! Try something else!", 'alert alert-danger')
            return redirect(url_for("index"))

    return render_template('home.html', form=form)



@app.route('/logout')
@login_required
def logout():
    session['logged_in'] = False 
    session.pop('logged_in', )
    flash('You were logged out.', 'alert alert-success')
    return redirect(url_for('index'))


@app.errorhandler(404)
@app.route('/error')
def page_not_found(error):

    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 500

