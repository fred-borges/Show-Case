from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializar o SQLAlchemy, o Migrate e o LoginManager
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()