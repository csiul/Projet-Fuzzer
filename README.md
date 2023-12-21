# Projet-Fuzzer

## Usage
Exécuter les commandes suivantes :
```bash
cd web
python3 configure.py # Pour créer les fichiers d'environnements de Flask
docker-compose up
```

Afin de tester le code modifié, exécuter les commandes suivantes :
```bash
docker-compose up --build # Reconstruit tous les conteneurs (peut être long inutilement)

# ou
docker-compose build web # Reconstruit le conteneur web seulement
docker-compose build api # Reconstruit le conteneur api seulement
docker-compose up

# ou
docker-compose build web && docker-compose up # One-liner
```

## Boilerplate
[Flask-Backbone sur abstractkitchen.com](https://abstractkitchen.com/blog/flask-backbone/)

[flask-backbone - GitHub](https://github.com/abstractkitchen/flask-backbone)

Les blueprints **about** et **index_page** sont des exemples provenant du boilerplate, et qui sont exclus de l'analyse de Pylint. 

## Installation de wpgarlic et utilisation
WPGarlic est installé et automatiquement utilisé par l'API, qui offre une couche d'abstraction.

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

> La vérification des imports a été désactivé dû au concept de sous-projets actuellement.

## API
L'API est basé sur FastAPI, qui offre par défaut une documentation automatiquement générée, via SwaggerUI ou Redoc.

La documentation ReDoc est désactivée présentement, car SwaggerUI est plus clair et mieux organisé.

URL de la documentation auto-générée : http://localhost:5050/docs
