"""
Initialisation de la gestion des erreurs.
"""
import typing as t

from flask import render_template, Flask


def register_error_handlers(app: Flask) -> None:
    """
    Enregistre le gestionnaire d'erreurs dans l'application.
    :param app: Application Flask
    """

    @app.errorhandler(404)
    def handle_error(exception) -> str:
        return render_template("error-pages/404.jinja2",
                               exception=exception)
