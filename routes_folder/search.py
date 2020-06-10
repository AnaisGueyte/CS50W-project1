
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


#search for books by author, title, isbn 

####################### SEARCH #######################

class SearchBookForm(Form):
    title = StringField('Title')
    author = StringField('Author')
    isbn = StringField('ISBN')
    submit = SubmitField('')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():

	form = SearchBookForm(request.form)

	book = Book()

	if request.method == 'GET':
		return render_template('/search.html', form=form)
	
	if request.method == 'POST' and form.validate():
		title = form.title.data
		author = form.author.data
		isbn = form.isbn.data

		if title:

			search = "%{}%".format(title)
			book = Book.query.filter(Book.title.like(search)).all()
			book_total = Book.query.filter(Book.title.like(search)).count()

			book_word = getBookWord(book_total)

			flash(str(book_total) + ' ' + book_word + ' found with title: ' + title, 'alert alert-success')
			return render_template('/search.html', form=form, results=book)


		elif author:

			search = "%{}%".format(author)
			book = Book.query.filter(Book.author.like(search)).all()
			book_total = Book.query.filter(Book.author.like(search)).count()

			book_word = getBookWord(book_total)

			flash(str(book_total) + ' ' + book_word + ' found with author: ' + author, 'alert alert-success')
			return render_template('/search.html', form=form, results=book)

		elif isbn:
			search = "%{}%".format(isbn)
			book = Book.query.filter(Book.isbn.like(search)).all()
			book_total = Book.query.filter(Book.isbn.like(search)).count()

			flash( str(book_total) + ' book found with ISBN: ' + isbn, 'alert alert-success')
			return render_template('/search.html', form=form, results=book)

	else:
		flash('oh oh something wrong', 'alert alert-danger')
		return render_template('/search.html', form=form, results=book)


	return render_template('/search.html', form=form)


def getBookWord(book_total):

	if book_total >= 2:
		book_word = 'books'
	else:
		book_word = 'book'

	return book_word





