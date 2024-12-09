from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Cambiar 'templates' por 'views' para indicar la nueva carpeta de plantillas
    app = Flask(__name__, template_folder='views')  # Cambiar 'templates' a 'views'

    # Set the SECRET_KEY for sessions and flash messages
    app.config['SECRET_KEY'] = os.urandom(24)  # Generates a random secret key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app