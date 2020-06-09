from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, EqualTo, Length, NoneOf, ValidationError

from user import User

# check login password
def check_password(form, password):
	# get user trying to log in
	user = User.find_by_username(request.form["username"])

	# if user exists and his password is correct
	if not user or not user.verify_password(password.data):
		raise ValidationError("Incorrect Username or Password!")

# registration form
class RegistrationForm(FlaskForm):
	# username -> input type - string, required
	username = StringField("username", [InputRequired()])

	# email -> input type - email, required
	email = EmailField("email", [InputRequired()])

	# password -> input type - password, required, at least 8 characters long
	password = PasswordField("password", [InputRequired(), Length(min=8, message="Password must be at least 8 characters!")])

	# confirm -> input type - password, equal to password
	confirm = PasswordField("confirm", [EqualTo("password", message="Passwords must match!")])

# login form
class LoginForm(FlaskForm):
	# email -> input type - email, required
	username = StringField("username", [InputRequired(message="Email is required!")])

	# password -> input type - password, verification if password is correct in db
	password = PasswordField("password", [InputRequired(message="Password is required"), check_password])