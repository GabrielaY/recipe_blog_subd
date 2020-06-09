from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, EqualTo, Length, NoneOf, ValidationError, Optional

from user import User

def check_password(form, password):
	user = User.find_by_username(request.form["username"])

	if not user or not user.verify_password(password.data):
		raise ValidationError("Incorrect Username or Password!")

class RegistrationForm(FlaskForm):
	username = StringField("username", [InputRequired()])
	email = EmailField("email", [InputRequired()])
	password = PasswordField("password", [InputRequired(), Length(min=8, message="Password must be at least 8 characters!")])
	confirm = PasswordField("confirm", [EqualTo("password", message="Passwords must match!")])

class EditProfileForm(FlaskForm):
	username = StringField("username", [InputRequired()])
	email = EmailField("email", [InputRequired()])
	password = PasswordField("password", [Optional(), Length(min=8, message="Password must be at least 8 characters!")])
	confirm = PasswordField("confirm", [EqualTo("password", message="Passwords must match!")])

class LoginForm(FlaskForm):
	username = StringField("username", [InputRequired(message="Email is required!")])
	password = PasswordField("password", [InputRequired(message="Password is required"), check_password])