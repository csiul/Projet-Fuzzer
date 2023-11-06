"""
Classe principale du module.
"""
import os
import shutil
import subprocess
from pathlib import Path

import requests

from .utils import get_file_hash


class WPFuzzer:
    """
    Abstraction de WPGarlic sous forme de classe.
    La classe offre également des méthodes utilitaires liées aux plugins WordPress.
    """

    def __init__(self, root_dir: str):
        """
        Initialisation.
        S'occupe d'installer WPGarlic à la source du projet lorsque nécessaire.
        :param root_dir Chemin absolu du répertoire racine à utiliser
        """
        self.root_dir = root_dir

        # Clone wpgarlic if not already present
        if not Path(f'{self.root_dir}/wpgarlic').is_dir():
            subprocess.run(["git", "clone", "https://github.com/kazet/wpgarlic.git", f'{self.root_dir}/wpgarlic'],
                           check=False)

        # Copy files needed in wpgarlic directory
        if (get_file_hash(f'{os.path.dirname(__file__)}/replacements/print_findings.py') !=
                get_file_hash(f'{self.root_dir}/wpgarlic/print_findings.py')):
            shutil.copyfile(f'{os.path.dirname(__file__)}/replacements/print_findings.py',
                            f'{self.root_dir}/wpgarlic/print_findings.py')

    def fuzz_plugin(self):
        pass

    def get_plugins_list(self) -> list:
        """
        Obtient la liste des plugins sur le site de WordPress.
        :return: Liste des plugins
        """
        endpoint = "https://api.wordpress.org/plugins/info/1.2/"
        page = 1
        plugins = []
        while True:
            print(page)
            params = {
                "action": "query_plugins",
                "request[per_page]": 250,  # number of plugins per page
                "request[page]": page
            }

            response = requests.get(endpoint, params=params, timeout=30)
            data = response.json()
            plugins += data['plugins']
            if page < data['info']['pages']:
                page += 1
            else:
                break

        return plugins
