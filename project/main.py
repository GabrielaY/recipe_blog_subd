# python imports
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from functools import wraps
import os

# imports from .py files
from user import User
from form_config import check_password, RegistrationForm, LoginForm, EditProfileForm

# app config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

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
	return render_template("index.html")

# register page
@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegistrationForm()

	# if form is valid
	if form.validate_on_submit():
		# get value and create user
		values = (
			None,
			request.form["username"],
			request.form["email"],
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

	# set default username and email
	form.username.data = user.username
	form.email.data = user.email

	# if form is valid
	if form.validate_on_submit():
		# get user info and save it
		user.username = request.form["username"]
		if(request.form["password"] != ''):
			user.password = User.hash_password(request.form["password"])

		user.save()

		return redirect("/tasks")

	# template edit_profile form
	return render_template("edit_profile.html", form=form, user=user)