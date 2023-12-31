"""
Modèle de base.
"""

from string import capwords
import re

from sqlalchemy import Column, ForeignKey, String, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql.base import INTEGER
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from ...utils import camel_to_snake


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

    uid: user id and primary key. Automatically generated
    email: email address of the user. Must be unique and follow the ULaval email address format
    password: password of the user. Must be hashed using set_password() method
    username: username of the user. Must be unique, alphanumeric, start with 2 letters
        and between 4 and 32 characters long
    first_name: first name of the user. Must be alphabetic and between 1 and 32 characters long
    last_name: last name of the user. Must be alphabetic and between 1 and 32 characters long
    profile_description: description of the user's profile. Must be between 0 and 512 characters long
    """
    # pylint: disable=R0902
    _uid = id_column()
    _email = Column(String(64),
                    CheckConstraint("REGEXP_LIKE(_email, '^([a-z[-] ])+[.]([a-z[-] ])+([.][0-9]*)?@ulaval[.]ca$')"),
                    nullable=True, unique=True)
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

    # pylint: disable=R0913
    def __init__(self, password: str, username: str, first_name: str,
                 last_name: str, email: str = None, profile_description: str = None) -> None:
        """
        Constructor.
        :param email: email address of the user
        :param password: password of the user
        :param username: username of the user
        :param first_name: first name of the user
        :param last_name: last name of the user
        :param profile_description: profile description of the user
        """
        self.email = email
        self.password = password
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.profile_description = profile_description

    @hybrid_property
    def uid(self) -> int:
        """
        UID getter.
        :return: UID of the user
        """
        return self._uid

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
        is_valid_email, criteria = User.validate_email(email)
        if is_valid_email:
            self._email = email
        else:
            raise ValueError(criteria)

    @classmethod
    def validate_email(cls, email: str) -> tuple[bool, dict[str, bool]]:
        """
        Checks if the email address is valid. Criteria are:

        :param email: email address. Must follow the ULaval email address format
        :return: tuple with the first element being True if the email address is valid, False otherwise
            and the second element being a tuple with the invalid criteria
        """
        if email is None:
            return True, {}
        is_valid = {
            "L'adresse courriel doit respecter le format de l'université Laval":
                bool(re.match(r'^([a-z\- ])+\.([a-z\- ])+(\.[0-9]*)?@ulaval\.ca$', email) is not None)
        }
        return all(is_valid.values()), is_valid

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
        is_strong_password, criteria = User.validate_password(password)
        if is_strong_password:
            self._password = generate_password_hash(password)
        else:
            raise ValueError(criteria)

    @classmethod
    def validate_password(cls, password) -> tuple[bool, dict[str, bool]]:
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
            and the second element being a tuple with the invalid criteria
        """
        is_valid = {
            "Le mot de passe doit être entre 8 et 32 caractères":
                bool(8 <= len(password) <= 32),
            "Le mot de passe doit contenir au moins 1 lettre minuscule":
                bool(any(char.islower() for char in password)),
            "Le mot de passe doit contenir au moins 1 lettre majuscule":
                bool(any(char.isupper() for char in password)),
            "Le mot de passe doit contenir au moins 1 chiffre":
                bool(any(char.isdigit() for char in password)),
            "Le mot de passe doit contenir au moins 1 caractère spécial":
                bool(any(not char.isalnum() for char in password))
        }
        return all(is_valid.values()), is_valid

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
        is_valid_username, criteria = User.validate_username(username)
        if is_valid_username:
            self._username = username
        else:
            raise ValueError(criteria)

    @classmethod
    def validate_username(cls, username: str) -> tuple[bool, dict[str, bool]]:
        """
        Checks if the username is valid. Criteria are:
        - Between 4 and 32 characters long
        - Starts with 2 letters
        - Only alphanumeric characters

        :param username: username
        :return: tuple with the first element being True if the username is valid, False otherwise
            and the second element being a tuple with the invalid criteria
        """
        is_valid = {
            "Le nom d'utilisateur doit être entre 4 et 32 caractères":
                bool(4 <= len(username) <= 32),
            "Le nom d'utilisateur doit commencer par 2 lettres":
                bool(username[:2].isalpha()),
            "Le nom d'utilisateur ne doit contenir que des caractères alphanumériques":
                bool(username.isalnum())
        }
        return all(is_valid.values()), is_valid

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
        is_valid_first_name, criteria = User.validate_first_name(first_name)
        if is_valid_first_name:
            self._first_name = capwords(first_name)
        else:
            raise ValueError(criteria)

    @classmethod
    def validate_first_name(cls, first_name: str) -> tuple[bool, dict[str, bool]]:
        """
        Checks if the first name is valid. Criteria are:
        - Between 1 and 32 characters long
        - Only alphabetic characters

        :param first_name: first name
        :return: tuple with the first element being True if the first name is valid, False otherwise
            and the second element being a tuple with the invalid criteria
        """
        is_valid = {
            "Le prénom doit être entre 1 et 32 caractères":
                bool(1 <= len(first_name) <= 32),
            "Le prénom ne doit contenir que des caractères alphabétiques":
                bool(first_name.isalpha())
        }
        return all(is_valid.values()), is_valid

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
        is_valid_last_name, criteria = User.validate_last_name(last_name)
        if is_valid_last_name:
            self._last_name = capwords(last_name)
        else:
            raise ValueError(criteria)

    @classmethod
    def validate_last_name(cls, last_name: str) -> tuple[bool, dict[str, bool]]:
        """
        Checks if the last name is valid. Criteria are:
        - Between 1 and 32 characters long
        - Only alphabetic characters

        :param last_name: last name
        :return: tuple with the first element being True if the last name is valid, False otherwise
            and the second element being a tuple with the invalid criteria
        """
        is_valid = {
            "Le nom de famille doit être entre 1 et 32 caractères":
                bool(1 <= len(last_name) <= 32),
            "Le nom de famille ne doit contenir que des caractères alphabétiques":
                bool(last_name.isalpha())
        }
        return all(is_valid.values()), is_valid

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
        is_valid_profile_description, criteria = User.validate_profile_description(profile_description)
        if is_valid_profile_description:
            self._profile_description = profile_description
        else:
            raise ValueError(criteria)

    @classmethod
    def validate_profile_description(cls, profile_description: str) -> tuple[bool, tuple[str, ...]]:
        """
        Checks if the profile description is valid. Criteria are:
        - Between 0 and 512 characters long
        - Can be null

        :param profile_description: profile description
        :return: tuple with the first element being True if the profile description is valid, False otherwise
            and the second element being a tuple with the invalid criteria
        """
        if profile_description is None:
            return True, tuple()
        is_valid = {
            "La description du profil doit être entre 0 et 512 caractères ou null":
                bool(0 <= len(profile_description) <= 512 or profile_description is None)
        }
        return all(is_valid.values()), tuple(key for key, value in is_valid.items() if not value)

    @hybrid_property
    def privileges(self) -> relationship:
        """
        Privileges getter.
        :return: relationship with Privilege model
        """
        return self._privileges


class Privilege(db.Model):
    """
    Model for user privileges. Allows users to have different allowed actions.

    email: email address of the user. Is foreign key. Domain must be @ulaval.ca
    privilege: privilege of the user. Must be one of the following:
        - admin: can do everything

    is related to User model
    """
    _uid = Column(ForeignKey("user._uid"), primary_key=True)
    _privilege = Column(String(32), nullable=False, primary_key=True)

    def __init__(self, uid: int = None, privilege: str = None) -> None:
        """
        Constructor.
        :param uid: uid of the user
        :param privilege: privilege of the user
        """
        if uid is not None:
            self.uid = uid
        if privilege is not None:
            self.privilege = privilege

    @hybrid_property
    def uid(self) -> int:
        """
        UID getter.
        :return: UID of the user
        """
        return self._uid

    @uid.setter
    def uid(self, uid: int) -> None:
        """
        UID setter.
        :param uid: uid of the user
        """
        self._uid = uid

    @hybrid_property
    def privilege(self) -> str:
        """
        Privilege getter.
        :return: privilege
        """
        return self._privilege

    @privilege.setter
    def privilege(self, privilege: str) -> None:
        """
        Privilege setter.
        :param privilege: privilege
        :raises ValueError: if privilege is not valid
        """
        is_valid_privilege, criteria = Privilege.validate_privilege(privilege)
        if is_valid_privilege:
            self._privilege = privilege
        else:
            raise ValueError(criteria)

    @classmethod
    def validate_privilege(cls, privilege: str) -> tuple[bool, dict[str, bool]]:
        """
        Checks if the privilege is valid. Criteria are:
        - Must be one of the following:
            - admin

        :param privilege: privilege
        :return: tuple with the first element being True if the privilege is valid, False otherwise
            and the second element being a tuple with the invalid criteria
        """
        is_valid = {
            "Le privilège doit être un de: admin":
                bool(privilege in ['admin'])
        }
        return all(is_valid.values()), is_valid
