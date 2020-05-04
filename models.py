from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

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
  def register(cls, username, pwd):
    hashed = bcrypt.generate_password_hash(pwd)
    hashed_utf8 = hashed.decode("utf8")
    return cls(username=username, password=hashed_utf8)

  @classmethod
  def authenticate(cls, username, pwd):
    u = User.query.filter_by(username=username).first()
    if u and bcrypt.check_password_hash(u.password, pwd):
      return u
    else:
      return False


