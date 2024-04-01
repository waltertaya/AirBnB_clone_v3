#!/usr/bin/python3
""" Flask app """

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exception):
    """ Close storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Not found error """
    return {"error": "Not found"}, 404


if __name__ == '__main__':
    """ Main Function """
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=getenv('HBNB_API_PORT', 5000), threaded=True)
