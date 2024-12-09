from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from gestor_pagos.app.routes import register_blueprints

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)
    return app
