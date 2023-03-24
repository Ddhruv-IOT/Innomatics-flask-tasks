from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask import jsonify
import pyshorteners
from datetime import datetime
from urllib.parse import urlparse


app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    user_data = db.relationship('UserData', backref='User', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.String(2550))
    output_data = db.Column(db.String(2550))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Link the UserData to the User using a foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('UserData', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'input': self.input_data,
            'output': self.output_data
        }


@app.before_first_request
def create_tables():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['pwd']
        user = User.query.filter_by(username=username).first()
        if not user or not user.password == password:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return render_template("index.html", username=username)
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['pwd']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('login'))
        if (len(username) >=5 and len(username) <=9):
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash('User created')
                return redirect(url_for('login'))
        else:
                flash("The username must be between 5 to 9 chars only!")
                return render_template("register.html")
             
    return render_template("register.html")

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def short_url(url):
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(url)
        return short_url

@app.route("/short", methods=["GET", "POST"])
@login_required
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        op = is_valid_url(user_input)
        if op == True:
                output = short_url(user_input)
                user_data = UserData(input_data=user_input,
                                output_data=output, user=current_user)
                db.session.add(user_data)
                db.session.commit()
                return render_template("index.html", s_url=output, username=current_user.username, op=True)
        else:
                flash("The given URL is not correct!")
                return render_template("index.html", s_url=user_input, username=current_user.username, op=op)


    return render_template("index.html")

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
        user_data = UserData.query.filter_by(user_id=current_user.id).all()
        ln = len(user_data)
        return render_template("history.html", user_data=user_data, len=ln)


if __name__ == "__main__":
    app.run(debug=True)
