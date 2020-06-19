from database import DB

class Ingredient:
	# initialise
	def __init__(self, id, recipe_id, name, quantity, units):
		self.id = id;
		self.recipe_id = recipe_id
		self.name = name;
		self.quantity = quantity;
		self.units = units;

	def create(self, db):
		values = (self.recipe_id, self.name, self.quantity, self.units)
		db.execute(
			'''INSERT INTO ingredients (recipe_id, name, quantity, units) VALUES (?, ?, ?, ?)''', values)

	# update ingredient info
	def save(self, db):
		values = (self.name, self.quantity, self.units, self.id)
		db.execute(
			'''UPDATE ingredients SET name = ?, quantity = ?, units = ? WHERE id = ?''', values)

	@staticmethod
	def get_by_recipe_id(recipe_id):
		with DB() as db:
			rows = db.execute('''
				SELECT * FROM ingredients WHERE recipe_id = ?
			''', (recipe_id, )).fetchall()

			if rows:
				return [Ingredient(*row) for row in rows]

