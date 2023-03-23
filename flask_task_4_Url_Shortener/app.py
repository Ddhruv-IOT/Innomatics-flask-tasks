from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
        return "<h1>Hello There</h1>"

@app.route("/1", methods=["GET", "POST"])
def page():
        return render_template("base.html")

@app.route("/register", methods=["GET", "POST"])
def page2():
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)