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

## Usage docker-compose
Exécuter les commandes suivantes :
```bash
python3 configure.py
docker-compose up
```

Afin de tester le code modifié, exécuter les commandes suivantes :
```bash
docker-compose up --build # Reconstruit tous les conteneurs (uniquement web pour l'instant)

# ou
docker-compose build web # Reconstruit le conteneur web seulement
docker-compose up
```

## Boilerplate
[Flask-Backbone sur abstractkitchen.com](https://abstractkitchen.com/blog/flask-backbone/)

[flask-backbone - GitHub](https://github.com/abstractkitchen/flask-backbone)

Les blueprints **about** et **index_page** sont des exemples provenant du boilerplate, et qui sont exclus de l'analyse de Pylint. 

## Installation de wpgarlic et utilisation
WPGarlic est installé et automatiquement utilisé par le module `wpfuzzer`, qui offre une couche d'abstraction.

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
