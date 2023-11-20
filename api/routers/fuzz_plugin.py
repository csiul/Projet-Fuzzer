"""
Router : Fuzz Plugin
"""

import subprocess
from enum import Enum, auto

from fastapi import APIRouter

from jobs.watch_wpgarlic import WatchWPGarlic

router = APIRouter(prefix='/fuzz_plugin', tags=['fuzz_plugin'])

router.wpgarlic_process = None


class FuzzerState(Enum):
    """
    États possible du Fuzzer
    """
    NOT_STARTED = auto()
    BUILDING = auto()
    FUZZING = auto()


@router.post('/{plugin_name}')
def fuzz(plugin_name: str):
    """
    Démarre le fuzzer sur un plugin.
    :param plugin_name: Nom (slug name) du plugin WordPress
    """
    if router.wpgarlic_process is None:
        # pylint: disable=consider-using-with
        # L'utilisation de with (context manager) n'est pas viable puisque le processus roule en background
        router.wpgarlic_process = subprocess.Popen(['python', 'fuzz_plugin.py', plugin_name], cwd='./wpgarlic/',
                                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        WatchWPGarlic(router.wpgarlic_process, on_finish=callback).start()
    else:
        return "Already fuzzing, go away..."
    return f'Fuzzer started with plugin {plugin_name}'


def callback():
    """
    Callback lorsque WPGarlic a terminé son exécution.
    """
    router.wpgarlic_process = None


@router.get('/state')
def get_fuzzer_state():
    """
    Obtient l'état actuel du Fuzzer.
    """
    if router.wpgarlic_process is None:
        return FuzzerState.NOT_STARTED.name
    return FuzzerState.FUZZING.name
