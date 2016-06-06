from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)

  def __init__(self, username, email):
    self.username = username
    self.email = email

  def __repr__(self):
    return '<User %r>' % self.username

  @app.route("/users")
  def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)


  @app.route("/users/create", methods=['POST', 'GET'])
  def create():
    if request.method == "POST":
      print(request.form)
      username = request.form['username']
      email = request.form['email']
      new_user = User(username, email)
      db.session.add(new_user)
      db.session.commit()
      return redirect('/users')
    return render_template("create.html")

  @app.route("/users/read/<int:user_id>")
  def read(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('read.html', user=user)

  @app.route("/users/update/<int:user_id>", methods=['POST', 'GET'])
  def update(user_id):
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
      id = request.form['user_id']
      user = User.query.filter_by(id=id).first()
      username = request.form['username']
      email = request.form['email']

      user.username = username
      user.email = email
      db.session.add(user)
      db.session.commit()

      return redirect('/users')

    return render_template('update.html', user=user)

  @app.route("/delete")
  def delete():
    pass

if __name__ == "__main__":
  app.run()