import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''

	CREATE TABLE IF NOT EXISTS users (
		username TEXT PRIMARY KEY NOT NULL,
		password TEXT NOT NULL
	)

''')
conn.cursor().execute('''

	CREATE TABLE IF NOT EXISTS recipes (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		owner TEXT NOT NULL,
		name TEXT NOT NULL,
		description TEXT,
		instructions TEXT NOT NULL,
		category_name TEXT NOT NULL,
		image_path TEXT NOT NULL,
		special_diet TEXT,
		UNIQUE(owner, name),
		FOREIGN KEY(owner) REFERENCES users(username)
	)

''')
conn.cursor().execute('''

	CREATE TABLE IF NOT EXISTS ingredients (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		recipe_id INTEGER NOT NULL,
		name TEXT NOT NULL,
		quantity FLOAT(4, 2) NOT NULL,
		units TEXT NOT NULL,
		UNIQUE(recipe_id, name),
		FOREIGN KEY(recipe_id) REFERENCES recipes(id)
	)

''')

conn.cursor().execute('''

	CREATE TABLE IF NOT EXISTS ratings (
		rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
		recipe_id INTEGER NOT NULL,
		user TEXT NOT NULL,
		rating INTEGER NOT NULL,
		CHECK (rating >= 1 AND rating <= 5),
		UNIQUE(user, recipe_id),
		FOREIGN KEY(user) REFERENCES users(username),
		FOREIGN KEY(recipe_id) REFERENCES recipes(id)
	)

''')
conn.commit()

class DB:
	def __enter__(self):
		self.conn = sqlite3.connect(DB_NAME)
		return self.conn.cursor()

	def __exit__(self, type, value, traceback):
		self.conn.commit()