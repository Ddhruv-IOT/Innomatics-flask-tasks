from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
        return render_template("register.html")

@app.route("/short", methods=["GET", "POST"])
def index():
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)