"""
More on this stuff
https://flask.palletsprojects.com/en/2.1.x/patterns/sqlalchemy/
https://docs.sqlalchemy.org/en/14/orm/session_basics.html#session-getting
"""

from flask import Flask
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.ext.sqlalchemy.model import db, User


def init_database(app: Flask) -> None:
    """
    Initialise la base de données.
    :param app: Application Flask
    """

    db.init_app(app)
    with app.app_context():
        db.session.configure()
        """
        Drop all tables. Only for development mode. If tables are altered in production, we should 
        use migrations instead.
        """
        db.drop_all()
        db.create_all()
        # Create admin user for testing purposes
        user = User(email="admin@admin",
                    first_name="admin",
                    last_name="admin",
                    username="admin")
        user.set_password("admin")
        db.session.add(user)
        db.session.commit()
