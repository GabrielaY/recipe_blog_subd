import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''

	CREATE TABLE IF NOT EXISTS users (
		Id INTEGER PRIMARY KEY AUTOINCREMENT,
		Username TEXT NOT NULL,
		Email TEXT NOT NULL,
		Password TEXT NOT NULL
	)

''')

conn.commit()

class DB:
	def __enter__(self):
		self.conn = sqlite3.connect(DB_NAME)
		return self.conn.cursor()

	def __exit__(self, type, value, traceback)
		self.conn.commit()