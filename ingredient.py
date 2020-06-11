from database import DB

class Ingredient:
	# initialise
	def __init__(self, recipe_id, name, quantity, units):
		self.recipe_id = recipe_id
		self.name = name;
		self.quantity = quantity;
		self.units = units;