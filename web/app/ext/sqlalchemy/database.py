"""
More on this stuff
https://flask.palletsprojects.com/en/2.1.x/patterns/sqlalchemy/
https://docs.sqlalchemy.org/en/14/orm/session_basics.html#session-getting
"""

from flask import Flask
import json
from app.ext.sqlalchemy.model import db, User, Privilege


def init_database(app: Flask) -> None:
    """
    Initialise la base de données.
    :param app: Application Flask
    """
    db.init_app(app)
    with app.app_context():
        db.session.configure()
        # Drop all tables. Only for development mode. If tables are altered in production, we should
        # use migrations instead.
        if not app.config.get('IS_PRODUCTION'):
            db.drop_all()
            db.create_all()
            with open("/run/secrets/app_admin") as f:
                admin_info = json.load(f)
                admin = User(**admin_info)
                admin_privilege = Privilege(admin.uid, privilege="admin")
                admin.privileges.append(admin_privilege)
                db.session.add(admin)
                db.session.commit()
