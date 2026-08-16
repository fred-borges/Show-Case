from flask import Flask, render_template
from .extensions import db, migrate, login_manager
import os
from dotenv import load_dotenv
from app.routes.users import user_bp
from app.routes.projects import post_bp
from flask_login import login_required

load_dotenv()


def criar_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config.from_object("config.Config")
    
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    
    db.init_app(app)
    migrate.init_app(app, db)
    from .models.users import User
    from .models.projects import Project
    
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    @app.route("/")
    @login_required
    def inicio():
        return render_template("home.html")

    return app