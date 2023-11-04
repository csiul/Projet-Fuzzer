# Projet-Fuzzer

## Usage
> Utiliser Linux ou WSL, Windows ne semble pas supporter WSGI

1. Activer venv ou similaire
2. Exécuter les commandes suivantes :
```bash
pip install -r requirements.txt
python3 configure.py # Pour initialiser les fichiers de configuration
flask run
```

## Usage Dockerfile
Exécuter les commandes suivantes :
```bash
python3 configure.py
docker image build -t project-fuzzer .
docker run -p PORT_LOCAL:FLASK_RUN_PORT -d project-fuzzer # où PORT_LOCAL correspond au port local souhaitant être utilisé pour accèder à l'app et où FLASK_RUN_PORT correspond à la valeur de FLASK_RUN_PORT dans le fichier .env
```

## Boilerplate
[Flask-Backbone sur abstractkitchen.com](https://abstractkitchen.com/blog/flask-backbone/)

[flask-backbone - GitHub](https://github.com/abstractkitchen/flask-backbone)

Les blueprints **about** et **index_page** sont des exemples provenant du boilerplate, et qui sont exclus de l'analyse de Pylint. 

## Pour utiliser wpgarlic
Exécuter cette commande :
```bash
python setup.py
```
Ou celles-ci :
```bash
chmod +x setup.sh
./setup.sh
```
Cela utilisera la version de `print_findings.py` qui écrit les résultats du fuzzer dans le fichier `output.json`.

## Pylint
Chaque Pull Request ou Push sur `master` déclenche une vérification GitHub Action qui exécute Pylint sur tous les fichiers .py du projet. 

Pour exécuter PyLint en développement
```bash
pip install pylint
pylint $(git ls-files '*.py')
```
Le fichier `pylintrc` contient les configurations utilisées par PyLint. 
La plupart des configurations sont les valeurs par défaut. 

Certains fichiers sont exclus, comme le contenu du dossier `config/` et les fichiers `print_findings.py` et `configure.py`.
Certains fichiers provenant du boilerplate sont également exclus, car le code ne provient pas de l'équipe.

Les codes données par Pylint lors des vérifications (par exemple C0114 pour le message `C0114: Missing module docstring (missing-module-docstring)`)
peuvent être recherchés sur la [documentation officielle de Pylint](https://pylint.readthedocs.io/en/latest/user_guide/messages/index.html).
