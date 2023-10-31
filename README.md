# Projet-Fuzzer

## Usage
> Utiliser Linux ou WSL, Windows ne semble pas supporter WSGI

1. Activer venv ou similaire
2. Exécuter les commandes suivantes :
```bash
pip -r requirements.txt
python3 configure.py # Pour initialiser les fichiers de configuration
flask run
```

## Boilerplate
[Flask-Backbone sur abstractkitchen.com](https://abstractkitchen.com/blog/flask-backbone/)

[flask-backbone - GitHub](https://github.com/abstractkitchen/flask-backbone)

## Pour utiliser wpgarlic
Exeécuter cette commande :
```bash
python setup.py
```
Ou celles-ci :
```bash
chmod +x setup.sh
./setup.sh
```
Cela utilisera la version de `print_findings.py` qui écrit les résultats du fuzzer dans le fichier `output.json`.
