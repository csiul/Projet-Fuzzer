"""
More on this stuff
https://flask.palletsprojects.com/en/2.1.x/patterns/sqlalchemy/
https://docs.sqlalchemy.org/en/14/orm/session_basics.html#session-getting
"""

from flask import Flask
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.ext.sqlalchemy.model import db
from flask_sqlalchemy import SQLAlchemy


def init_database(app: Flask) -> None:
    """
    Initialise la base de données.
    :param app: Application Flask
    """

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception) -> None:

        # https://docs.sqlalchemy.org/en/14/orm/contextual.html#using-thread-local-scope-with-web-applications
        db.session.remove()
