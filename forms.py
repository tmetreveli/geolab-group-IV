from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import IntegerField, EmailField, PasswordField, StringField, SubmitField,FileField


class AddProductForm(FlaskForm):
    name = FileField("Name", validators=[DataRequired(message="Please enter a name.")])
    colour = StringField("Colour", validators=[DataRequired()])
    mood = StringField("Mood", validators=[DataRequired()])
    submit = SubmitField("Add")

class RegisterForm(FlaskForm):
    name = StringField("Enter name", validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField("Enter your password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    name = StringField("Enter name", validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField("Enter your password", validators=[DataRequired()])
    submit = SubmitField("Login")