#!/usr/bin/python3
"""
app.py module
"""
from models import storage
from flask import Flask
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exc):
    """Close database"""
    storage.close()


if __name__ == "__main__":
    """Main function"""
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
