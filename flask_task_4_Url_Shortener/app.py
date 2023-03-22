from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
        return "<h1>Hello There</h1>"

@app.route("/1", methods=["GET", "POST"])
def page():
        return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)