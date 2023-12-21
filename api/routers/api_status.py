"""
Router : Status
"""
from dataclasses import dataclass
import subprocess
from pathlib import Path
from typing import Dict

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


@dataclass
class APIStatus:
    """
    Modèle utilisé pour retourner le status de l'API.
    """
    checks: Dict[str, bool]
    result: bool


@router.get('/')
def get_status():
    """
    Obtient le statut actuel de l'API.
    """
    checks = {
        'wpgarlic_root': Path('wpgarlic').is_dir(),
        'wpgarlic_exec': Path('wpgarlic/fuzz_plugin.py').is_file(),
        'docker': check_if_command_exists(['docker', 'version']),
        'docker-compose': check_if_command_exists(['docker-compose', 'version'])
    }
    return APIStatus(checks=checks, result=all(value for value in checks.values()))
