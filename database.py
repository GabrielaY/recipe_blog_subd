import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''

	CREATE TABLE IF NOT EXISTS users (
		username TEXT PRIMARY KEY,
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
			quantity FLOAT(2, 1) NOT NULL,
			units TEXT NOT NULL,
			UNIQUE(recipe_id, name),
			FOREIGN KEY(recipe_id) REFERENCES recipes(id)

		)
	
''')

conn.cursor().execute('''

	CREATE TABLE IF NOT EXISTS ratings (
		rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
		recipe_id INTEGER NOT NULL,
		user_id INTEGER NOT NULL,
		rating INTEGER,
		CHECK (rating >= 1 AND rating <= 5),
		UNIQUE(user_id, recipe_id),
		FOREIGN KEY(recipe_id) REFERENCES users(user_id),
		FOREIGN KEY(rating_id) REFERENCES recipes(recipe_id)

	)

''')
conn.commit()

class DB:
	def __enter__(self):
		self.conn = sqlite3.connect(DB_NAME)
		return self.conn.cursor()

	def __exit__(self, type, value, traceback):
		self.conn.commit()