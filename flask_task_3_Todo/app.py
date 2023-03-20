from flask import Flask, render_template, request

app = Flask(__name__)

notes = []


# added GET method to display the page for the first time in browser.
@app.route('/', methods=["GET", "POST"])
def index():
    """Function to process the GET or POST request"""

    # if a POST request is made, then form data will be processed 
    if request.method == "POST":  

        # changed request.args to request.form, 
        # as the data was collected using HTML form and sent over POST request
        note = request.form.get("note")
        notes.append(note)

        # update the web page with the processed form data
        return render_template("home.html", notes=notes)

    # the template page to be displayed over GET request.
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
