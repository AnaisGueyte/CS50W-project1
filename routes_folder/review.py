
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


#Leave a review for a book 

####################### REVIEW #######################

class ReviewBookForm(Form):
	note = SelectField('Note', choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired("Please, leave a note")])
	review = TextAreaField('Review',validators=[DataRequired("Please, leave a review")])
	submit = SubmitField('')


@app.route('/review/add/<string:isbn>', methods=['GET', 'POST'])
@login_required
def add_review(isbn):

	form = ReviewBookForm(request.form)
	book = Book()
	book = Book.query.filter(Book.isbn == isbn).first()

	if request.method == 'GET':
		return render_template('/add_review.html', form=form, book=book)

	if request.method == 'POST' and form.validate():
		review = Review()

		review.note = form.note.data
		review.review = form.review.data
		review.review_date = date.today()
		review.isbn = isbn
		review.username = session['username'] 

		db.session.add(review)
		db.session.commit()

		flash('Review for "' + book.title + '" was successfully added'  , 'alert alert-success')
		return redirect(url_for('search'))

	return render_template('/add_review.html', form=form, book=book)







