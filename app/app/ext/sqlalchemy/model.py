"""
Modèle de base.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql.base import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from string import capwords

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

    _email = Column(String(64), nullable=False, unique=True, primary_key=True)
    _password = Column(String(102), nullable=False)
    _username = Column(String(32),
                       CheckConstraint("REGEXP_LIKE(_username, '^([a-zA-Z]{2}([a-zA-Z]|[0-9]){2}([a-zA-Z]|[0-9])*)$')"),
                       nullable=False, unique=True)
    _first_name = Column(String(32),
                         CheckConstraint("REGEXP_LIKE(_first_name, '^[a-zA-Z]+$')"), nullable=False)
    _last_name = Column(String(32),
                        CheckConstraint("REGEXP_LIKE(_last_name, '^[a-zA-Z]+$')"), nullable=False)
    _profile_description = Column(String(512), nullable=True)

    _privileges = relationship("Privilege", backref="user")

    @hybrid_property
    def email(self) -> str:
        """
        Email getter.
        :return: email address
        """
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        """
        Email setter.
        :param email: email address
        """
        is_valid_email, criteria = User._validate_email(email)
        if is_valid_email:
            self._email = email
        else:
            raise ValueError(criteria)

    @classmethod
    def _validate_email(cls, email: str) -> tuple[bool, tuple[str, ...]]:
        """
        Checks if the email address is valid. Criteria are:

        :param email: email address
        :return: tuple with the first element being True if the email address is valid, False otherwise
            and the second element being a dictionary with the invalid criteria
        """
        # TODO: add email validation
        return True, tuple()

    @hybrid_property
    def password(self) -> str:
        """
        Password getter.
        :return: hashed password
        """
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        """
        Password setter. Hashes the password using werkzeug.security library.
        :param password: password to hash
        :return: None
        :raises ValueError: if password is not strong enough
        """
        is_strong_password, criteria = User._check_password_strength(password)
        if is_strong_password:
            self._password = generate_password_hash(password)
        else:
            raise ValueError(criteria)

    @classmethod
    def _check_password_strength(cls, password) -> tuple[bool, tuple[str, ...]]:
        """
        Checks if the password is strong enough. Criteria are:
        - At least 8 characters long
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one number
        - At least one special character
        - Maximum 32 characters long

        :param password: plain text password
        :return: tuple with the first element being True if the password is strong enough, False otherwise
            and the second element being a dictionary with the invalid criteria
        """
        is_valid = {
            "Le mot de passe doit être entre 8 et 32 caractères":
                True if 8 <= len(password) <= 32 else False,
            "Le mot de passe doit contenir au moins 1 lettre minuscule":
                True if any(char.islower() for char in password) else False,
            "Le mot de passe doit contenir au moins 1 lettre majuscule":
                True if any(char.isupper() for char in password) else False,
            "Le mot de passe doit contenir au moins 1 chiffre":
                True if any(char.isdigit() for char in password) else False,
            "Le mot de passe doit contenir au moins 1 caractère spécial":
                True if any(not char.isalnum() for char in password) else False
        }
        return all(is_valid.values()), tuple(key for key, value in is_valid.items() if not value)

    def check_password(self, password):
        """
        Checks if the plain text password matches the hashed password.
        :param password: plain text password
        :return: True if the passwords match, False otherwise
        """
        return check_password_hash(self.password, password)

    @hybrid_property
    def username(self) -> str:
        """
        Username getter.
        :return: username
        """
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        """
        Username setter.
        :param username: username
        :raises ValueError: if username is not valid
        """
        is_valid_username, criteria = User._validate_username(username)
        if is_valid_username:
            self._username = username
        else:
            raise ValueError(criteria)

    @classmethod
    def _validate_username(cls, username: str) -> tuple[bool, tuple[str, ...]]:
        """
        Checks if the username is valid. Criteria are:
        - Between 4 and 32 characters long
        - Starts with 2 letters
        - Only alphanumeric characters

        :param username: username
        :return: tuple with the first element being True if the username is valid, False otherwise
            and the second element being a dictionary with the invalid criteria
        """
        is_valid = {
            "Le nom d'utilisateur doit être entre 4 et 32 caractères":
                True if 4 <= len(username) <= 32 else False,
            "Le nom d'utilisateur doit commencer par 2 lettres":
                True if username[:2].isalpha() else False,
            "Le nom d'utilisateur ne doit contenir que des caractères alphanumériques":
                True if username.isalnum() else False
        }
        return all(is_valid.values()), tuple(key for key, value in is_valid.items() if not value)

    @hybrid_property
    def first_name(self) -> str:
        """
        First name getter.
        :return: first name
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        """
        First name setter.
        :param first_name: first name
        :raises ValueError: if first name is not valid
        """
        is_valid_first_name, criteria = User._validate_first_name(first_name)
        if is_valid_first_name:
            self._first_name = capwords(first_name)
        else:
            raise ValueError(criteria)

    @classmethod
    def _validate_first_name(cls, first_name: str) -> tuple[bool, tuple[str, ...]]:
        """
        Checks if the first name is valid. Criteria are:
        - Between 1 and 32 characters long
        - Only alphabetic characters

        :param first_name: first name
        :return: tuple with the first element being True if the first name is valid, False otherwise
            and the second element being a dictionary with the invalid criteria
        """
        is_valid = {
            "Le prénom doit être entre 1 et 32 caractères":
                True if 1 <= len(first_name) <= 32 else False,
            "Le prénom ne doit contenir que des caractères alphabétiques":
                True if first_name.isalpha() else False
        }
        return all(is_valid.values()), tuple(key for key, value in is_valid.items() if not value)

    @hybrid_property
    def last_name(self) -> str:
        """
        Last name getter.
        :return: last name
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str) -> None:
        """
        Last name setter.
        :param last_name: last name
        :raises ValueError: if last name is not valid
        """
        is_valid_last_name, criteria = User._validate_last_name(last_name)
        if is_valid_last_name:
            self._last_name = capwords(last_name)
        else:
            raise ValueError(criteria)

    @classmethod
    def _validate_last_name(cls, last_name: str) -> tuple[bool, tuple[str, ...]]:
        """
        Checks if the last name is valid. Criteria are:
        - Between 1 and 32 characters long
        - Only alphabetic characters

        :param last_name: last name
        :return: tuple with the first element being True if the last name is valid, False otherwise
            and the second element being a dictionary with the invalid criteria
        """
        is_valid = {
            "Le nom de famille doit être entre 1 et 32 caractères":
                True if 1 <= len(last_name) <= 32 else False,
            "Le nom de famille ne doit contenir que des caractères alphabétiques":
                True if last_name.isalpha() else False
        }
        return all(is_valid.values()), tuple(key for key, value in is_valid.items() if not value)

    @hybrid_property
    def profile_description(self) -> str:
        """
        Profile description getter.
        :return: profile description
        """
        return self._profile_description

    @profile_description.setter
    def profile_description(self, profile_description: str) -> None:
        """
        Profile description setter.
        :param profile_description: profile description
        :raises ValueError: if profile description is not valid
        """
        is_valid_profile_description, criteria = User._validate_profile_description(profile_description)
        if is_valid_profile_description:
            self._profile_description = profile_description
        else:
            raise ValueError(criteria)

    @classmethod
    def _validate_profile_description(cls, profile_description: str) -> tuple[bool, tuple[str, ...]]:
        """
        Checks if the profile description is valid. Criteria are:
        - Between 0 and 512 characters long
        - Can be null

        :param profile_description: profile description
        :return: tuple with the first element being True if the profile description is valid, False otherwise
            and the second element being a dictionary with the invalid criteria
        """
        is_valid = {
            "La description du profil doit être entre 0 et 512 caractères ou null":
                True if 0 <= len(profile_description) <= 512 or profile_description is None else False
        }
        return all(is_valid.values()), tuple(key for key, value in is_valid.items() if not value)


class Privilege(db.Model):
    """
    Model for user privileges. Allows users to have different allowed actions.

    email: email address of the user. Is foreign key. Domain must be @ulaval.ca
    privilege: privilege of the user. Must be one of the following:
        - admin: can do everything

    is related to User model
    """
    email = Column(ForeignKey("user._email"), primary_key=True)
    privilege = Column(String(32), nullable=False, primary_key=True)