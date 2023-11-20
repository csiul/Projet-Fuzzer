"""
Router : Status
"""

import subprocess
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix='/status', tags=['status'])


def check_if_command_exists(command: [str]) -> bool:
    """
    Vérifie si une commande console existe.
    ATTENTION, la commande est réellement exécutée, privilégier les commandes pour obtenir des versions,
    qui n'affectent pas le système.
    :param command: Commande à exécuter, sous forme d'array. Ex. ['ls', '-la']
    :return: Vrai si la commande a pu être exécutée, faux si FileNotFoundError (commande inconnue)
    """
    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
    except FileNotFoundError:
        return False

    return True


@router.get('/')
def get_status():
    """
    Obtient le statut actuel de l'API.
    """
    return {
        'wpgarlic': {
            'root': Path('wpgarlic').is_dir(),
            'exec': Path('wpgarlic/fuzz_plugin.py').is_file()
        },
        'docker': check_if_command_exists(['docker', 'version']),
        'docker-compose': check_if_command_exists(['docker-compose', 'version'])
    }
