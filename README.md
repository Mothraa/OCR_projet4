# Script d'extraction des prix de books.toscrape.com

## À propos

Formation OpenClassRooms - Developpeur d'application python - Projet 4

Développez un programme logiciel en Python (POO + design pattern MVC)
Application de gestion de tournois d'échec


## Prérequis

Python >=3.12.1

## Installation

Cloner le repository
```bash
git clone https://github.com/Mothraa/OCR_projet4.git
```
Créer l'environnement avec [venv](https://docs.python.org/fr/3/library/venv.html)
```bash
python -m venv env
```
Activer l'environnement

- sous linux ou mac
```bash
source env/bin/activate
```
- sous windows
```bash
env/scripts/activate
```
Utiliser le gestionnaire de package [pip](https://docs.python.org/fr/dev/installing/index.html) pour installer les librairies python
```bash
pip install -r requirements.txt
```

## Utilisation

Executer le script main.py
dans le terminal :
```bash
python main.py
```

## Langages & Frameworks

Développé sous python 3.12.1
avec l'aide de la librairie :
- [Faker](https://faker.readthedocs.io/en/master/) pour la génération de données aléatoires

## Documentation

### Table des matières

  - [Création de joueurs](#players)
  - [Création de tournois](#tournaments)
  - [Affichage de rapports](#reports)
  - [Organisation des données](#datastructure)

### Création de joueurs

xxxx

* *xxxx* : xxxx, **xxxx**


### Création de tournois

xxxx

### Affichage de rapports

xxxx

#### Organisation des données

xxxx

#### Arborescence

xxx
```bash
\output\[category_name]\[export_date]-[category_name]-list.csv
                       \images\[id_upc].jpg
                               ...
```
Exemple :
```bash
\output\mystery_3\20240125-mystery_3-list.csv
                 \images\0c7b9cf2b7662b65.jpg
```

## Gestion des versions

La dénomination des versions suit la spécification décrite par la [Gestion sémantique de version](https://semver.org/lang/fr/)

Les versions disponibles ainsi que les journaux décrivant les changements apportés sont disponibles depuis [la section releases](https://github.com/Mothraa/OCR_projet4/releases)

## Licence

Voir le fichier [LICENSE](./LICENSE.md) du dépôt.