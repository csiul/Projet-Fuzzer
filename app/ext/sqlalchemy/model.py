"""
Modèle de base.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.dialects.postgresql.base import INTEGER

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
