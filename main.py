from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def elements():
    return render_template("about.html")


@app.route("/ordering")
def generic():
    return render_template("ordering.html")



if __name__ == "__main__":
    app.run(debug=True)