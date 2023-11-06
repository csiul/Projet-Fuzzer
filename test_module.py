"""
Test du module wpfuzzer.
À retirer après avoir testé.
"""
import os.path

from wpfuzzer.wpfuzzer import WPFuzzer

w = WPFuzzer(os.path.dirname(__file__))
print(w.get_plugins_list())
