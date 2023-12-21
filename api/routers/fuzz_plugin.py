"""
Router : Fuzz Plugin
"""
import json
import os
import shutil
import subprocess
from enum import Enum, auto

from fastapi import APIRouter, HTTPException

from jobs.watch_process import WatchProcess
from routers.wordpress import check_if_plugin_exists

router = APIRouter(prefix='/fuzz_plugin', tags=['fuzz_plugin'])

router.wpgarlic_process = None
router.wpgarlic_results = {}


class FuzzerState(Enum):
    """
    États possible du Fuzzer
    """
    NOT_STARTED = auto()
    BUILDING = auto()
    FUZZING = auto()


@router.post('/{plugin_name}', status_code=202)
def fuzz(plugin_name: str):
    """
    Démarre le fuzzer sur un plugin.
    :param plugin_name: Nom (slug name) du plugin WordPress
    """
    if router.wpgarlic_process is not None:
        raise HTTPException(status_code=409,
                            detail=f'The fuzzer is already fuzzing "{router.wpgarlic_process.args[-1]}".')
    if plugin_name in router.wpgarlic_results:
        raise HTTPException(status_code=403, detail='This plugin has already been fuzzed.')
    check_if_plugin_exists(plugin_name)  # Lance une exception si non trouvé

    # pylint: disable=consider-using-with
    # L'utilisation de with (context manager) n'est pas viable puisque le processus roule en background
    router.wpgarlic_process = subprocess.Popen(['python', 'fuzz_plugin.py', plugin_name], cwd='./wpgarlic/',
                                               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    WatchProcess(router.wpgarlic_process, on_finish=callback, args=plugin_name).start()

    return {'message': f'Fuzzer started with plugin {plugin_name}'}


def callback(slug):
    """
    Callback lorsque WPGarlic a terminé son exécution.
    """
    router.wpgarlic_process = None
    subprocess.run(['python', 'print_findings.py', 'data/plugin_fuzz_results/'],
                   cwd='./wpgarlic/',
                   check=False,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    shutil.move(os.getcwd() + '/wpgarlic/data/output.json',
                f'{os.getcwd()}/wpgarlic/data/scanned_results/{slug}.json')
    router.wpgarlic_results[slug] = f'{os.getcwd()}/wpgarlic/data/scanned_results/{slug}.json'
    subprocess.run(['docker-compose', 'down'],
                   cwd='./wpgarlic/',
                   check=False,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


@router.get('/state')
def get_fuzzer_state():
    """
    Obtient l'état actuel du Fuzzer.
    """
    if router.wpgarlic_process is None:
        return FuzzerState.NOT_STARTED.name
    return FuzzerState.FUZZING.name


@router.get('/results/{plugin_name}')
def get_plugin_results(plugin_name: str):
    """
    Obtient les résultats filtrés d'un plugin.
    :param plugin_name: Nom du plugin
    """
    if plugin_name not in router.wpgarlic_results:
        raise HTTPException(status_code=404, detail="Plugin not found in fuzzed plugins history")
    return json.load(open(router.wpgarlic_results[plugin_name], 'r', encoding='utf-8'))


@router.get('/history')
def get_scanned_plugins():
    """
    Obtient la liste des plugins déjà traités par le Fuzzer.
    """
    return {
        'data': list(router.wpgarlic_results.keys())
    }
