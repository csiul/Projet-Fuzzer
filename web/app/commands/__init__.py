"""
Commandes Flask personnalisées
"""
from flask import Flask

from app.commands.application import app_cli


def init_app_cli(app: Flask) -> None:
    """
    Commandes utilitaires pour le développement Flask.
    :param app: Application Flask
    """
    app.cli.add_command(app_cli)
