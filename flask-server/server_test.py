# This file is just to set up the server and make sure it's working
from flask import Flask

app = Flask(__name__)

# Practice API Route

@app.route("/practice")

def practice():
    return { "practice": ["Test text 1", "Test text 2", "Test text 3"]}


@app.route("/add", methods=["POST"], strict_slashes=False)

def add():
    return "based"

if __name__ == "__main__":
    app.run(debug=True)