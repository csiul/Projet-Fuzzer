"""
Utilitaires sur le système de fichiers.
"""
import glob
import os
import shutil
import typing as t
from pathlib import Path
from string import Template


def create_folder_if_not(folder_path: str) -> None:
    """
    Crée un dossier s'il n'existe pas.
    :param folder_path: Chemin du dossier
    """
    return os.makedirs(os.path.dirname(folder_path), exist_ok=True)


def list_files(directory: str, **kwargs) -> t.List[str]:
    """
    Liste les fichiers d'un dossier.
    :param directory: Chemin du dossier
    :param kwargs: Arguments supplémentaires (ignore, file_extension)
    :return: Liste des fichiers
    """
    ignore: list = kwargs.get("ignore", [""])
    file_extension: t.Union[str, None] = kwargs.get("file_extension")

    files: list = []

    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if file not in ignore:
                if file_extension and file.endswith(file_extension):
                    files.append(file)

                elif not file_extension:
                    files.append(file)

    return files


def list_directories(directory: str, ignore: t.Union[None, list] = None) -> t.List[str]:
    """
    Liste les doissiers d'un dossier parent.
    :param directory: Chemin du dossier parent
    :param ignore: Dossiers à ignorer
    :return: Liste des dossiers
    """
    if not ignore:
        ignore: list = ["__pycache__"]

    return list(
        filter(
            lambda x: os.path.isdir(os.path.join(directory, x)) and x not in ignore,
            os.listdir(directory)
        )
    )


def set_file(file_path: str, file_content: str) -> None:
    """
    Change le contenu d'un fichier.
    :param file_path: Chemin du fichier
    :param file_content: Contenu à appliquer
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
        f.close()


def has_file(file_path: str) -> bool:
    """
    Vérifie l'existence d'un fichier.
    :param file_path: Chemin du fichier potentiel
    :return: Vrai si c'est un fichier, faux sinon
    """
    potential_file = Path(file_path)

    return potential_file.is_file()


def copy_file(src: str, dest: str) -> str:
    """
    Copie un fichier.
    :param src: Source
    :param dest: Destination
    :return: Résultat de shutil.copy
    """
    return shutil.copy(src, dest)


def read_file(file_path: str) -> t.IO:
    """
    Lit le contenu d'un fichier.
    :param file_path: Chemin du fichier
    :return: Contenu du fichier
    """
    return open(file_path, 'r', encoding='utf-8')


def replace_templates_in_files(
        lookup_path: str, file_extension: str, template_vars: dict, ignore: t.Union[None, t.List[str]] = None) -> None:
    """
    Remplace les valeurs dans un fichier selon les templates.
    :param lookup_path: Chemin où chercher les fichiers
    :param file_extension: Extension des fichiers à chercher
    :param template_vars: Dictionnaire des valeurs de template à remplacer
    :param ignore: Fichier à ignorer
    """
    if not ignore:
        ignore: list = []

    files: t.List[str] = [f for f in glob.glob(f"{lookup_path}/**/*{file_extension}", recursive=True)]

    for f in files:
        if f.split("/")[-1] not in ignore:
            file_content = Template(read_file(f).read()).substitute(template_vars)
            set_file(f, file_content)
