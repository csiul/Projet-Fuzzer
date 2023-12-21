"""
https://flask.palletsprojects.com/en/2.2.x/templating/#context-processors

"""

from flask import Flask


def register_context_processor(app: Flask) -> None:
    """
    Enregistre le contexte du processeur.
    :param app: Application Flask
    """

    @app.context_processor
    def inject_is_production() -> dict:
        return {
            'application_name': "Flask-Backbone"
        }
