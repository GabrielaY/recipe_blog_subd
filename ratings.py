from database import DB

class ratings:
	# initialise
	def __init__(self, recipe_id, rating_id, user_id, rating):
		self.recipe_id = recipe_id;
		self.rating_id = rating_id
		self.user_id = user_id;
		self.rating = rating;

	def create(self):
		with DB() as db:
			values = (self.recipe_id, self.rating_id, self.user_id, self.rating)
			db.execute(
				'''INSERT INTO ratings (recipe_id, rating_id, user_id, rating) VALUES (?, ?, ?)''', values)

	# update ingredient info
	def save(self):
		with DB() as db:
			values = (self.rating, self.rating_id)
			db.execute(
				'''UPDATE ratings SET rating = ? WHERE rating_id = ?''', values)


	# get latest rate
	def latest_rate(self):
        with DB() as db:
        	values = (self.recipe_id)
            rows = db.execute('SELECT * FROM rating WHERE recipe_id = ?', values).fetchone()
            return rating


