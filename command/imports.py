from application import app, db
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from models import *

import csv


@app.route('/import')
def import_books():

    with open('books.csv', 'r') as inFile:
        reader = csv.reader(inFile, dialect='excel', delimiter=';')
        commentsList = [row for row in reader]

        for row in commentsList:
            for values in row:

                book = Book()

                result = [x.strip() for x in values.split(',')]
                book.isbn = result[0]
                book.title = result[1]
                book.author = result[2]
                book.year = result[3]

                db.session.add(book)
                db.session.commit()

    flash('Import done', 'alert alert-success')
    return redirect(url_for('index'))