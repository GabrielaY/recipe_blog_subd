import hashlib

from database import DB

class User:
	# initialise
	def __init__(self, username, password):
		self.username = username
		self.password = password

	# add to database
	def create(self):
		with DB() as db:
			values = (self.username, self.password)
			db.execute(
				'''INSERT INTO users (username, password) VALUES (?, ?)''', values)

	# update user info
	def save(self):
		with DB() as db:
			values = (self.password, self.username)
			db.execute(
				'''UPDATE users SET password = ? WHERE username = ?''', values)

	# find user by email
	@staticmethod
	def find_by_username(username):
		if not username:
			return None
		with DB() as db:
			row = db.execute(
				'''SELECT * FROM users WHERE username = ?''', (username,)).fetchone()
			if row:
				return User(*row)

	# hash user's password
	@staticmethod
	def hash_password(password):
		return hashlib.sha256(password.encode('utf-8')).hexdigest()

	# verify user's password on login
	def verify_password(self, password):
		return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()