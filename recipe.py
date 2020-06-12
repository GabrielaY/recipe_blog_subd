from database import DB

class Recipe:
	# initialise
	def __init__(self, id, owner, name, description, instructions, category_name, image_path, special_diet):
		self.id = id;
		self.owner = owner;
		self.name = name;
		self.description = description;
		self.instructions = instructions;
		self.category_name = category_name;
		self.image_path = image_path;
		self.special_diet = special_diet;

	# add to database
	def create(self):
		with DB() as db:
			values = (self.owner, self.name, self.description, self.instructions, self.category_name, self.image_path, self.special_diet)
			db.execute(
				'''INSERT INTO recipes (owner, name, description, instructions, category_name, image_path, special_diet) VALUES (?, ?, ?, ?, ?, ?, ?)''', values)

	# update recipe info
	def save(self):
		with DB() as db:
			values = (self.name, self.description, self.instructions, self.image_path, self.id)
			db.execute(
				'''UPDATE recipes SET name = ?, description = ?, instructions = ?, image_path = ? WHERE id = ?''', values)

	# find recipe by id
	@staticmethod
	def find_by_id(id):
		with DB() as db:
			row = db.execute(
				'''SELECT * FROM recipes WHERE id = ?''', (id,)).fetchone()
			if row:
				return Recipe(*row)

	# find recipes by category
	@staticmethod
	def find_by_category(category_name):
		with DB() as db:
			rows = db.execute(
				'SELECT * FROM recipes WHERE category_name = ?',
				(category_name,)
			).fetchall()
			return [Recipe(*row) for row in rows]

	# find recipes by special diet (vegeterian or vegan)
	@staticmethod
	def find_by_diet(diet_name):
		with DB() as db:
			rows = db.execute(
				'SELECT * FROM recipes WHERE special_diet = ?',
				(diet_name,)
			).fetchall()
			return [Recipe(*row) for row in rows]

	# find recipes by ingredient
	@staticmethod
	def find_by_ingredient(ingredient_name):
		with DB() as db:
			ingredient_name = "%" + ingredient_name + "%"
			rows = db.execute('''
				SELECT recipes.* FROM recipes JOIN ingredients  ON recipes.id = ingredients.recipe_id and ingredients.name LIKE ?;
			''',(ingredient_name,)
			).fetchall()
			return [Recipe(*row) for row in rows]

	# get average rate for recipe
	def calc_avg_rate(self):
		rating = 0
		with DB() as db:
			values = (self.id,)
			rating_row = db.execute('SELECT AVG(rating) FROM ratings WHERE recipe_id = ?', values).fetchone()

			return rating_row[0]