from flask import Flask

from src.api import plant, question
from src.config import Config
from src.ext import db, migrate, api
from src.commands import init_db, populate_db
from src.models import Plant, Question

COMMANDS = [init_db, populate_db]

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)

    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

def register_commands(app):
    for cmd in COMMANDS:
        app.cli.add_command(cmd)