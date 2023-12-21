"""
Job : WatchWPGarlic
"""

from subprocess import Popen
from threading import Thread
from typing import Callable


class WatchProcess(Thread):
    """
    Job permettant de surveiller un processus et de détecter la fin d'exécution.
    Hérite de Thread, afin d'offrir des méthodes comme .start() et de directement pouvoir être exécuté en background.
    ATTENTION, ce thread consomme présentement beaucoup de ressources puisque la boucle n'a pas de sleep.
    """

    def __init__(self, process: Popen[bytes], on_finish: Callable, args):
        """
        Initialiser la job.
        :param process: Processus à surveiller, de type Popen
        :param on_finish: Fonction à appeler lorsque le processus est terminé
        """
        self.process = process
        self.on_finish = on_finish
        self.args = args
        super().__init__(target=self._task)

    def _task(self):
        """
        Lors du démarrage de la job.
        """
        while self.process is not None:  # Tant que le processus existe
            if self.process.poll() is not None:  # Vérification de l'état du processus
                self.process = None  # On détruit le processus (seulement en référence)
                self.on_finish(self.args)  # On appelle le callback
