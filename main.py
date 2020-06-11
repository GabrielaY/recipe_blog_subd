# python imports
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from functools import wraps
import os

# imports from .py files
from user import User
from recipe import Recipe
from form_config import check_password, RegistrationForm, LoginForm, EditProfileForm, CreateRecipeForm, EditRecipeForm


UPLOAD_FOLDER = "./static/images/"
# app config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

@app.before_first_request
def function_to_run_only_once():
	session["USERNAME"] = None
	session["SIGNED_IN"] = False

# require login config
def require_login(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		# if there isn't a logged user
		if not session.get("SIGNED_IN"):
			return redirect('/login')
		return func(*args, **kwargs)
	return wrapper

# main page
@app.route("/")
def main_page():
	return render_template("index.html", signed_in = session.get("SIGNED_IN"))

# register page
@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegistrationForm()

	# if form is valid
	if form.validate_on_submit():
		# get value and create user
		values = (
			request.form["username"],
			User.hash_password(request.form["password"])
		)
		User(*values).create()

		# get the user and put him in the session
		user = User.find_by_username(request.form["username"])
		session["SIGNED_IN"] = True
		session["USERNAME"] = request.form["username"]

		return redirect("/")

	# template the registration form
	return render_template("register.html", form=form)

# login page
@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()

	# if form is valid
	if form.validate_on_submit():
		# get the user and put him in the session
		user = User.find_by_username(request.form["username"])
		session["SIGNED_IN"] = True
		session["USERNAME"] = request.form["username"]

		return redirect("/")

	# template the login form
	return render_template("login.html", form=form)

# logout page
@app.route("/logout")
def logout():
	# remove user from the session
	session["SIGNED_IN"] = False
	session["USERNAME"] = None

	return redirect("/")

# edit user info
@app.route("/edit", methods=["GET", "POST"])
@require_login
def edit_profile():
	form = EditProfileForm()

	# get user, whose profile will be edited
	user = User.find_by_username(session.get("USERNAME"))

	# set default username
	form.username.data = user.username

	# if form is valid
	if form.validate_on_submit():
		# get user info and save it
		user.username = request.form["username"]
		session["USERNAME"] = user.username
		if(request.form["password"] != ''):
			user.password = User.hash_password(request.form["password"])

		user.save()

		return redirect("/")

	# template edit_profile form
	return render_template("edit_profile.html", form=form, user=user)

@app.route("/createRecipe", methods=["GET", "POST"])
@require_login
def create_recipe():
	form = CreateRecipeForm()

	# if form is valid
	if form.validate_on_submit():

		image = request.files["image"]
		path = os.path.join(UPLOAD_FOLDER, session.get("USERNAME"))

		# Check if path exists and create one if it doesn"t
		if not os.path.exists(path):
			os.makedirs(path)

		image.save(os.path.join(path, "KOZUNAK"))

		values = (
			None,
			session.get("USERNAME"),
			request.form["name"],
			request.form["description"],
			request.form["instructions"],
			request.form["category_name"],
			"static/images/" + request.form["name"],
			request.form["special_diet"]
		)
		Recipe(*values).create()

		# get the user and put him in the session
		return redirect("/")

	# template the registration form
	return render_template("create_recipe.html", form=form)

@app.route("/editRecipe/<id>", methods=["GET", "POST"])
@require_login
def edit_recipe(id):
	form = EditRecipeForm()

	recipe = Recipe.find_by_id(id)

	# set default username
	form.name.data = recipe.name
	form.description.data = recipe.description
	form.instructions.data = recipe.instructions

	# if form is valid
	if form.validate_on_submit():
		# get user info and save it
		recipe.name = request.form["name"]
		recipe.description = request.form["description"]
		recipe.instructions = request.form["instructions"]
		
		recipe.save()

		return redirect("/")

	# template edit_profile form
	return render_template("edit_recipe.html", form=form, recipe=recipe)
	
