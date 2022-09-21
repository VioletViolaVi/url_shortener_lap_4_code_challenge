from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(3))

    def __init__(self, long, short):
        self.long = long
        self.short = short


@app.before_first_request
def create_tables():
    db.create_all()


def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        # attaining long url
        url_attained = request.form["urlShortener"]
        # check if url exists
        existing_url = Urls.query.filter_by(long=url_attained).first()
        if existing_url:
            # return short url
            return redirect(url_for("display_shorten_url", url=existing_url.short))
        else:
            # if not, create short url, return & store in database
            short_url = shorten_url()
            new_url = Urls(url_attained, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_shorten_url", url=short_url))
    else:
        return render_template("home.html")


@app.route("/display/<url>")
def display_shorten_url(url):
    return render_template("short_url.html", display_short_url=url)


@app.route("/<short_url>")
def redirect_to_longer_url(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
