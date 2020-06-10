from flask import Flask
from flask import render_template, flash, redirect, request, url_for, jsonify, session, Response
from wtforms import Form, StringField, SubmitField, PasswordField, TextAreaField, BooleanField, DateField, SelectField, TextField, widgets, SelectMultipleField
from wtforms.validators import DataRequired
from application import app, db
from models import *
import routes
from datetime import datetime, date

from flask_login import login_required, login_user, login_manager
from flask_sqlalchemy import SQLAlchemy

import requests
import json
import re


#API call for books

####################### API CALL #######################

@app.route('/api/<string:isbn>', methods=['GET', 'POST'])
@login_required
def api_by_isbn(isbn):

	book = Book()
	book = Book.query.filter(Book.isbn == isbn).first()

	if book is None:
		return redirect(url_for('error'))
	else:
		res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "xBKc2kBrb6SrUUxzmEvXQ", "format": "json", "isbns": isbn})
		
		gr_reviews = ''
		average_ratings = 'N/A'
		reviews_count = 'N/A'
		
		if res.status_code == 200:
			gr_reviews = res.json()
			gr_reviews = gr_reviews['books'][0]
			average_ratings = gr_reviews['average_rating']
			reviews_count = gr_reviews['reviews_count']

		results = {}
		results['title'] = book.title
		results['author'] = book.author
		results['year'] = book.year
		results['isbn'] = book.isbn
		results['reviews_count'] = reviews_count
		results['reviews_score']  = average_ratings

		return jsonify(results)