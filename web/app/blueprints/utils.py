"""
Méthodes utilitaires globales pour les blueprints.
"""

import typing as t

from app.utils import filesystem

IGNORE_FOLDERS: t.List[str] = ["__pycache__", "__boilerplate__"]


def list_blueprints(blueprints_folder: str, cb: t.Union[t.Callable[[str], None], None] = None) -> t.List[str]:
    """
    Obtient la liste des blueprints.
    :param blueprints_folder: Dossier de blueprints à utiliser
    :param cb: Méthode optionnelle à appliquer sur les blueprints
    :return: Liste des blueprints
    """
    available_blueprints: t.List[str] = \
        filesystem.list_directories(blueprints_folder, IGNORE_FOLDERS)

    if cb:
        for blueprint_name in available_blueprints:
            cb(blueprint_name)

    return available_blueprints


def list_boilerplate_skeletons(boilerplate_folder: str) -> t.List[str]:
    """
    Obtient la liste des squelettes disponibles pour les blueprints.
    :param boilerplate_folder: Dossier à utiliser
    :return: Liste des squelettes
    """
    return filesystem.list_directories(boilerplate_folder + "/skeletons")


def list_boilerplate_models(boilerplate_folder: str) -> t.List[str]:
    """
    Obtient la liste des modèles.
    :param boilerplate_folder: Dossier à utiliser
    :return: Liste des modèles
    """
    return filesystem.list_files(
        boilerplate_folder + "/models", file_extension="py.template")
