from pinecone import Pinecone, ServerlessSpec
import flask
from flask_cors import CORS

app = flask.Flask(__name__, static_url_path='/static')
CORS(app)

CORS(app, resources={r"/": {"origins": "http://localhost:8080"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route("/")
def index() -> None:
    return flask.render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
