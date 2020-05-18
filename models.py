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
