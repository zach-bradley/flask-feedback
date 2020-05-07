from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'borkborkiamdog'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
db.create_all()

@app.route("/")
def home_page():
 return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
  if 'username' in session:
    return redirect(f"/users/{session['username']}")
  form = RegisterForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    user = User.register(username, password, first_name, last_name, email)
    db.session.add(user)
    db.session.commit()
    session["username"] = user.username
    return redirect(f"users/{user.username}")
  else: 
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    username = form.username.data
    pwd = form.password.data
    user = User.authenticate(username, pwd)
    if user:
      session['username'] = user.username
      flash(f"Welcome back, {session.username}", "success")
      return redirect(f"users/{user.username}")
    else:
      form.username.errors = ["That username doesn't exist"]
  return render_template("login.html", form=form)

@app.route("/logout")
def logout():
  session.pop("username")
  return redirect("/login")

########################
# User Routes
########################

@app.route("/users/<username>")
def user(username):
  if "username" not in session:
    flash("You must be logged in", "danger")
    return redirect("/")
  user = User.query.get(username)
  feedback = Feedback.query.filter_by(username=username)
  return render_template("user.html", user=user, feedback=feedback)

@app.route("/users/<username>/delete")
def delete_user(username):
  if "username" not in session or username != session['username']:
    flash("You need to be logged in to do that", "danger")
    return redirect('/login')
  else: 
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    flash("User successfully delete!", "success")
    return redirect("/login")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):  
  form = FeedbackForm()
  if 'username' not in session: 
    flash("You must be logged in to add feedback", "danger")
    return redirect("/login")
  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    feedback = Feedback(title=title, content=content, username=username)
    db.session.add(feedback)
    db.session.commit()
    flash("Added feedback!", "success")
    return redirect(f"/users/{username}")
  else: 
    return render_template("feedback.html", form=form, url=f'/users/{username}/feedback/add', verb="Add")

########################
# Feedback Routes
########################

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
  form = FeedbackForm()
  feedback = Feedback.query.get_or_404(feedback_id)
  if 'username' not in session:
    flash("You must be logged in to do that", "danger")
    return redirect("/login")  
  if form.validate_on_submit():
    feedback.title = form.title.data
    feedback.content = form.content.data
    db.session.add(feedback)
    db.session.commit()
    flash("Feedback Edited!", "success")
    return redirect(f"/users/{feedback.username}")
  else:
    form.title.data = feedback.title
    form.content.data = feedback.content
    return render_template("feedback.html", form=form, url=f'/feedback/{feedback.id}/update', verb="Edit")

@app.route("/feedback/<int:feedback_id>/delete")
def delete_feedback(feedback_id):
  if 'username' not in session:
    flash("You must be logged in to do that", "danger")
    return redirect("/login")   
  feedback = Feedback.query.get(feedback_id)
  db.session.delete(feedback)
  db.session.commit()
  flash("Feedback deleted!", "success")
  return redirect(f"/users/{feedback.username}")


