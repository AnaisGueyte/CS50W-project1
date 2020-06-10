
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, jsonify, session, Response
from wtforms import Form, StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from application import app, db
from models import *
import routes

from flask_login import login_required, login_user, login_manager
from flask_sqlalchemy import SQLAlchemy

import requests
import json
import re

#Show book details

####################### GET BOOK #######################

@app.route('/book/<string:isbn>', methods=['GET', 'POST'])
@login_required
def book_page(isbn):

	book = Book()
	book = Book.query.filter(Book.isbn == isbn).first()

	username = session['username'] 

	has_reviewed = Review.query.filter(Review.isbn == isbn, Review.username == username).all()

	if(has_reviewed):
		has_reviewed = True
	else:
		has_reviewed = False

	reviews = Review.query.filter(Review.isbn == isbn).all()
	
	
	gr_reviews = ''
	
	if res.status_code == 200:
		gr_reviews = res.json()
		gr_reviews = gr_reviews['books'][0]

	return render_template('/book_page.html', reviews=reviews, book=book, has_reviewed=has_reviewed, gr_reviews=gr_reviews)

