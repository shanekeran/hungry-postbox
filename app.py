import os
from flask import Flask
if os.path.exists("env.oy"):
    import env


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hi Shane"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)     # Set to False b4 submission.
