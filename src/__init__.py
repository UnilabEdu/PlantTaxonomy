from flask import Flask
from flask_admin.menu import MenuLink

from src.admin import register_admin_views, MyAdminIndexView
from src.api import plant, question
from src.config import Config
from src.ext import db, migrate, api, admin, login_manager
from src.commands import init_db, populate_db
from src.models import Plant, Question, User

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
    admin.init_app(app, index_view=MyAdminIndexView())
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    register_admin_views()

    admin.add_link(MenuLink(name='Logout', category='', url="/admin/logout"))

def register_commands(app):
    for cmd in COMMANDS:
        app.cli.add_command(cmd)