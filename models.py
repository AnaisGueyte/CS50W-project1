from application import app, db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Auth_user.query.get(id)

class Auth_user(UserMixin, db.Model):
	username = db.Column(db.String(500), primary_key=True)
	password = db.Column(db.String(500))

	def is_active(self):
		return True

	def get_id(self):
		return self.username

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False

	#def __repr__(self):
	#	return '<Auth_user {}>'.format(self.username)



class Book(db.Model):
	isbn = db.Column(db.String(500), primary_key=True)
	title = db.Column(db.String(500))
	author = db.Column(db.String(500))
	year = db.Column(db.String(500))

	def get_isbn(self):
		return self.isbn

	def get_title(self):
		return self.title

	def get_author(self):
		return self.author

	def get_year(self):
		return self.year

	#def __repr__(self):
	#	return '<book {}>'.format(self.title)


class Review(db.Model):
	review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	isbn = db.Column(db.String(500), primary_key=True)
	username = db.Column(db.String(500))
	note = db.Column(db.String(500))
	review = db.Column(db.String(500))
	review_date = db.Column(db.String(500))

	def get_isbn(self):
		return self.isbn

	def get_review(self):
		return self.review

	def get_username(self):
		return self.username

	def get_note(self):
		return self.note

	#def __repr__(self):
		#return '<review {}>'.format(self.review_id)

