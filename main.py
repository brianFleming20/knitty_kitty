from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from functools import wraps
# from forms import CreatePostForm


app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6briaWlSihBXox7C0sKR6b'


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kitty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        if current_user.is_anonymous:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


login_manager = LoginManager()
login_manager.init_app(app)


# User form data
class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    posts = relationship("KittyPost", back_populates="author")


class KittyPost(db.Model):
    __tablename__ = "kitty_posts"
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Key to link to the user's post
    author_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

# db.create_all()


# Create form for registration of new user
# class RegisterForm(FlaskForm):
#     name = StringField("Name", validators=[DataRequired()])
#     email = StringField("Email", validators=[DataRequired()])
#     password = StringField("Password", validators=[DataRequired()])
#     submit = SubmitField("Sign me up!")


# class UserLogin(FlaskForm):
#     email = StringField("Email", validators=[DataRequired()])
#     password = StringField("Password", validators=[DataRequired()])
#     submit = SubmitField("Log me in!")


class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    body = CKEditorField("Item Content", validators=[DataRequired()])
    submit = SubmitField("Update new item")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    now = date.today().strftime("%A %d %B %Y")
    # posts = KittyPost.query.all()
    # data = request.form.get('ckeditor')
    return render_template("index.html", date=now)


@app.route("/about")
def elements():
    return render_template("about.html")


@app.route("/ordering")
def generic():
    return render_template("ordering.html")


@app.route("/add-post")
def add_new_item():
    return render_template("add-post.html")


if __name__ == "__main__":
    app.run(debug=True)