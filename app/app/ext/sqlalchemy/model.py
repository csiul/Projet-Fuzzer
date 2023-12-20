"""
Modèle de base.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql.base import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.utils import camel_to_snake


def id_column() -> Column:
    """
    Génère une colonne ID.
    :return: Colonne
    """
    return Column(
        INTEGER,
        autoincrement=True,
        primary_key=True,
        nullable=False,
        unique=True
    )


def int_fk_column(foreign_key) -> Column:
    """
    Génère une colonne FK.
    :param foreign_key: Clé étrangère
    :return: Colonne
    """
    return Column(INTEGER, ForeignKey(foreign_key))


# pylint: disable=R0903
class _BaseModel:
    """
    this model will be used as a base for our future models
    you can customize with some boilerplate methods and/or properties
    you can also create multiple base models for different purposes

    With this configuration you can define your new models without __tablename__ parameter,
    but class name must be the same as a table name

    # for a table "currency"
    class CurrencyModel(BaseModel):
        ...

    # for a table "user_profile"
    class UserProfileModel(BaseModel):
        ...

    """

    @declared_attr
    def __tablename__(self) -> str:
        # pylint: disable=E1101
        return camel_to_snake(self.__name__).replace('_model', '')


BaseModel = declarative_base(cls=_BaseModel)

db = SQLAlchemy(model_class=BaseModel)


class User(db.Model):
    """
    Model for app users.
    Is related to Privilege model.

    Also provides methods to hash, check passwords and verify password strength.

    email: email address of the user and primary key. Domain must be @ulaval.ca
    password: password of the user. Must be hashed using set_password() method
    username: username of the user. Must be unique, alphanumeric, start with 2 letters
        and between 4 and 32 characters long
    first_name: first name of the user. Must be alphabetic and between 1 and 32 characters long
    last_name: last name of the user. Must be alphabetic and between 1 and 32 characters long
    profile_description: description of the user's profile. Must be between 0 and 512 characters long
    """

    email = Column(String(64), nullable=False, unique=True, primary_key=True)
    password = Column(String(102), nullable=False)
    username = Column(String(32),
                      CheckConstraint("REGEXP_LIKE(username, '^([a-zA-Z]{2}([a-zA-Z]|[0-9]){2}([a-zA-Z]|[0-9])*)$')"),
                      nullable=False, unique=True)
    first_name = Column(String(32),
                        CheckConstraint("REGEXP_LIKE(first_name, '^[a-zA-Z]+$')"), nullable=False)
    last_name = Column(String(32),
                       CheckConstraint("REGEXP_LIKE(last_name, '^[a-zA-Z]+$')"), nullable=False)
    profile_description = Column(String(512), nullable=True)

    privileges = relationship("Privilege", backref="user")

    def set_password(self, password):
        """
        Hashes the password using werkzeug.security library.
        :param password: password to hash
        :return: None
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the plain text password matches the hashed password.
        :param password: plain text password
        :return: True if the passwords match, False otherwise
        """
        return check_password_hash(self.password, password)

    @classmethod
    def check_password_strength(cls, password):
        """
        Checks if the password is strong enough. Criterias are:
        - At least 8 characters long
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one number
        - At least one special character
        - Maximum 32 characters long

        :param password: plain text password
        :return: tuple with the first element being True if the password is strong enough, False otherwise
            and the second element being a dictionary with the criterias and their validity
        """
        is_valid = {
            "length": True if 8 <= len(password) <= 32 else False,
            "lowercase": True if any(char.islower() for char in password) else False,
            "uppercase": True if any(char.isupper() for char in password) else False,
            "number": True if any(char.isdigit() for char in password) else False,
            "special": True if any(not char.isalnum() for char in password) else False
        }
        return all(is_valid.values()), is_valid


class Privilege(db.Model):
    email = Column(ForeignKey("user.email"), primary_key=True)
    privilege = Column(String(32), nullable=False, primary_key=True)
