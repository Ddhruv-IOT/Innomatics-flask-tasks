from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
        return "<h1>Hello There</h1>"


if __name__ == "__main__":
    print("Hi")
    app.run(debug=True)
    app.run(use_reloader=True)