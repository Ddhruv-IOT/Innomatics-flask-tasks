from flask import Flask, render_template, request
import re

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Main logic to take user input and compare with regexp"""

    # If form is submitted, process the data
    if request.method == 'POST':

        # Get user input
        test_string = request.form['test_string']
        regex_pattern = request.form['regex_pattern']

        # Use the re module to match the pattern in the test string
        matches = re.findall(str(regex_pattern), str(test_string))

        # Display the matched strings
        if matches:
            num_matches = len(matches)
            matched_strings = "\n".join(matches)
        else:
            matched_strings = "No matches found."
            num_matches = 0

        return render_template('index.html', matched_strings=matched_strings, num_matches=num_matches)

    # Display the page for the first time in browser over GET request
    return render_template('index.html')
