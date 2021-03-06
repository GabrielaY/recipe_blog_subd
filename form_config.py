from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SelectField, DecimalField, validators
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, EqualTo, Length, NoneOf, ValidationError, Optional

from user import User

def check_password(form, password):
	user = User.find_by_username(request.form["username"])

	if not user or not user.verify_password(password.data):
		raise ValidationError("Incorrect Username or Password!")

class RegistrationForm(FlaskForm):
	username = StringField("username", [InputRequired()])
	password = PasswordField("password", [InputRequired(), Length(min=8, message="Password must be at least 8 characters!")])
	confirm = PasswordField("confirm", [EqualTo("password", message="Passwords must match!")])

class EditProfileForm(FlaskForm):
	password = PasswordField("password", [InputRequired(), Length(min=8, message="Password must be at least 8 characters!")])
	confirm = PasswordField("confirm", [EqualTo("password", message="Passwords must match!")])

class LoginForm(FlaskForm):
	username = StringField("username", [InputRequired(message="Username is required!")])
	password = PasswordField("password", [InputRequired(message="Password is required"), check_password])

class CreateRecipeForm(FlaskForm):
	name = StringField("name", [InputRequired(message="Recipe name is required!")])
	description = StringField("description", [InputRequired(message = "You must add a description to your recipe!")])
	instructions = StringField("instructions", [InputRequired(message = "You must add instructions to your recipe!")])
	category_name = SelectField('category', choices=[('apetizer', 'Apetizer'), ('dessert', 'Dessert'), ('soup', 'Soup')])
	image = FileField('image')
	number_of_ingredients = DecimalField('number_of_ingredients')
	special_diet = SelectField('special_diet', choices=[('no_special_diet', 'No special diet'), ('vegan', 'Vegan'), ('vegeterian','Vegeterian')])

class EditRecipeForm(FlaskForm):
	name = StringField("name", [InputRequired(message="Recipe name is required!")])
	description = StringField("description", [InputRequired(message = "You must add a description to your recipe!")])
	instructions = StringField("instructions", [InputRequired(message = "You must add instructions to your recipe!")])
	image = FileField('image')
