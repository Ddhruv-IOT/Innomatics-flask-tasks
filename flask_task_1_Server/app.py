from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', '')
    upper_name = name.upper()
    return f'''
    <html>
        <head>
            <style>
                body {{
                    background-color: black;
                }}
                h1, h3 {{
                    text-align: center;
                    align-content: center;
                    justify-content: center;
                    color: white;
                    white-space: nowrap;
                    overflow: hidden;
                    animation: typing 5s steps(45, end);
                    text-shadow: 1px 1px blue;
                }}
                 @keyframes typing {{
                    from {{ width: 0; }}
                    to {{ width: 45ch; }}
                }}
                div {{
                    display:flex;
                    text-align: center;
                    align-items: center;
                    justify-content: center;
                    height: 80%;
                    flex-direction: column;
                }}
            </style>
        </head>
        <body>
        <div>
            <h1>Hello, {upper_name}!</h1>
            <h3> What's on your mind today ?</h3>
            </div>
        </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
