from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
  """Form to register a new user"""

  username = StringField("Username", validators=[InputRequired(message="Please enter a username")])
  password = PasswordField("Password", validators=[InputRequired(message="Please enter a password")])
  first_name = StringField("First Name", validators=[InputRequired(message="Please enter a first name")])
  last_name = StringField("Last Name", validators=[InputRequired(message="Please enter a last name")])
  email = StringField("Email", validators=[InputRequired(message="Please enter valid email")])

class LoginForm(FlaskForm):
  """Form for logging a user in"""

  username = StringField("Username", validators=[InputRequired(message="Please enter a username")])
  password = PasswordField("Password", validators=[InputRequired(message="Please enter a password")])

class FeedbackForm(FlaskForm):
  """form for adding feedback from a user"""

  title = StringField("Title", validators=[InputRequired(message="Must add a title")])
  content = StringField("Content", validators=[InputRequired(message="Must not be empty")])