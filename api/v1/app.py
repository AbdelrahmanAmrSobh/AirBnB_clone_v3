#!/usr/bin/python3
"""The app"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def TearDown(error):
    """Handle closing"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handle page not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """Run flask"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
