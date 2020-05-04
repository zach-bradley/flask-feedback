from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
 db.app=app
 db.init_app(app)

class User(db.Model):
 """User model"""

 __tablename__ = "users"
 id = db.Column(db.Integer, primary_key=True, autoincrement=True)

 def __repr__(self):
  return f"<User {self.id}>"