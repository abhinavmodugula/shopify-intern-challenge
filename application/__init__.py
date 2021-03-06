from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        from . import routes
        from .models import Item, Warehouse

        app.register_blueprint(routes.main_bp)
        db.create_all()

        return app