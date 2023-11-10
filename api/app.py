"""
API permettant d'utiliser WPGarlic.
"""

import subprocess
from enum import Enum, auto
from pathlib import Path
from threading import Thread

from fastapi import FastAPI

app = FastAPI(debug=True)

app.wpgarlic_process = None


class FuzzerState(Enum):
    """
    États possible du Fuzzer
    """
    NOT_STARTED = auto()
    BUILDING = auto()
    FUZZING = auto()


def check_if_command_exists(command: [str]) -> bool:
    """
    Vérifie si une commande console existe.
    :param command: Commande à exécuter, sous forme d'array. Ex. ['ls', '-la']
    :return: Vrai si la commande a pu être exécutée, faux si FileNotFoundError (commande inconnue)
    """
    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
    except FileNotFoundError:
        return False

    return True


@app.get("/status")
def get_status():
    """
    Obtient le statut actuel de l'API.
    L'API effectue des vérifications sur ses fichiers lors de cette requête.
    :return: JSON de l'état actuel
    """
    return {
        'wpgarlic': {
            'root': Path('wpgarlic').is_dir(),
            'exec': Path('wpgarlic/fuzz_plugin.py').is_file()
        },
        'docker': check_if_command_exists(['docker', 'version']),
        'docker-compose': check_if_command_exists(['docker-compose', 'version'])
    }


@app.post('/fuzz_plugin/{plugin_name}')
def fuzz(plugin_name: str):
    """
    Démarre le fuzzer sur un plugin.
    :param plugin_name: Nom (slug name) du plugin WordPress
    :return: Message d'erreur si le Fuzzer est déjà démarré, ou de confirmation si le Fuzzer a été démarré
    """
    if app.wpgarlic_process is None:
        # pylint: disable=consider-using-with
        # L'utilisation de with (context manager) n'est pas viable puisque le processus roule en background
        app.wpgarlic_process = subprocess.Popen(['python', 'fuzz_plugin.py', plugin_name], cwd='./wpgarlic/',
                                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        Thread(target=watch_fuzzer).start()
    else:
        return "Already fuzzing, go away..."
    return f'Fuzzer started with plugin {plugin_name}'


def watch_fuzzer():
    """
    Vérifie en boucle si le Fuzzer a terminé son exécution.
    """
    while app.wpgarlic_process is not None:
        if app.wpgarlic_process.poll() is not None:
            app.wpgarlic_process = None
            print('Fuzzing finished', flush=True)


@app.get('/fuzz_plugin/state')
def get_fuzzer_state():
    """
    Obtient l'état actuel du Fuzzer.
    :return: État actuel selon l'enum
    """
    if app.wpgarlic_process is None:
        return FuzzerState.NOT_STARTED.name
    return FuzzerState.FUZZING.name
