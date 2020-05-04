from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'borkborkiamdog'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
 return redirect("/register")

app.route("/r:egister", methods=["GET", "POST"])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    username = form.username.data
    pwd = form.password.data
    user = User.register(username, pwd)
    print(user)
    return redirect("/register")
  else: 
    return render_template("/register", form=form)