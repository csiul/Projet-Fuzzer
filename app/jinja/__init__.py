"""
Initialisation de Jinja.
"""

from flask import Flask

from app.jinja.filters import register_filters
from app.jinja.context_processor import register_context_processor


def register_jinja_mapping(app: Flask) -> None:
    """
    Enregistrement des mappings pour Jinja.
    :param app: Application Flask
    """
    register_filters(app)
    register_context_processor(app)
