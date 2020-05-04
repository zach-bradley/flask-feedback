from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, HiddenField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm)
  """Form to register a new user"""

  username = StringField("Username", validators=[InputRequired(message="Please enter a username")])
  password = HiddenField("Password", validators=[InputRequired(message="Please enter a password")])
  first_name = StringField("First Name", validators=[InputRequired(message="Please enter a first name")])
  last_name = StringField("Last Name", validators=[InputRequired(message="Please enter a last name")])