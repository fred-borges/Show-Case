from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .extensions import db, migrate


def criar_app():
    app = Flask(__name__)
    
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def inicio():
        return "Showcase funcionando!"

    return app