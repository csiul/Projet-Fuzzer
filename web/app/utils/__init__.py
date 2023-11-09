"""
Méthodes utilitaires globales.
"""

import re


def camel_to_snake(x: str) -> str:
    """
    Convertit un texte CamelCase en snakeCase.
    :param x: Texte à convertir
    :return: Texte modifié
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', x)

    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(word: str) -> str:
    """
    Convertit un mot snakeCase en CamelCase
    :param word: Mot à convertir
    :return: Mot modifié
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))
