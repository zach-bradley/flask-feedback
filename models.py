from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()



def connect_db(app):
 db.app=app
 db.init_app(app)

class User(db.Model):
  """User model"""

  __tablename__ = "users"
  username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
  password = db.Column(db.Text, nullable=False)
  email = db.Column(db.String(50), nullable=False)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)

  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"

  def __repr__(self):
    return f"<User {self.id} {self.username} {self.password} {self.email} {self.first_name} {self.last_name}>"

  @classmethod
  def register(cls, username, pwd, first_name, last_name, email):
    hashed = bcrypt.generate_password_hash(pwd)
    hashed_utf8 = hashed.decode("utf8")
    return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name, email=email)

  @classmethod
  def authenticate(cls, username, pwd):
    u = User.query.filter_by(username=username).first()
    if u and bcrypt.check_password_hash(u.password, pwd):
      return u
    else:
      return False


class Feedback(db.Model):
  """User feedback model"""

  __tablename__ = 'feedback'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)


