"""
Fonctions utilitaires pour le module.
"""

import hashlib


def get_file_hash(filepath: str) -> str:
    """
    Calcule le hash MD5 d'un fichier.
    :param filepath: Chemin du fichier
    :return: Hash MD5 sous forme hexadécimale
    """
    with open(filepath, "rb") as file:
        file_hash = hashlib.md5()
        while chunk := file.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()
