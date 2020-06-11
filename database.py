import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''

	CREATE TABLE IF NOT EXISTS users (
		username TEXT PRIMARY KEY,
		password TEXT NOT NULL
	),

	CREATE TABLE IF NOT EXISTS recipes (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		owner TEXT NOT NULL,
		name TEXT NOT NULL,
		description TEXT,
		instructions TEXT,
		category_name TEXT NOT NULL,
		image_path TEXT NOT NULL,
		special_diet TEXT,
		UNIQUE(owner_id, name),
		FOREIGN KEY(owner) REFERENCES users(username)

	),

	CREATE TABLE IF NOT EXISTS ingredients (
		recipe_id INTEGER NOT NULL,
		name TEXT NOT NULL,
		quantity FLOAT(2, 1) NOT NULL,
		units TEXT NOT NULL,
		UNIQUE(recipe_id, name),
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