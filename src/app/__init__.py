import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Set up logging to a file
    if not app.debug:
        handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

    with app.app_context():
        from . import routes
        return app
    
