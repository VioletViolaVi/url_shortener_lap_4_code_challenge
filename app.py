from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/say_hello")
def say_hello():
    return "Hello There 👋"


@app.route("/say_goodbye")
def say_goodbye():
    return "Bye Bye 👋"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
