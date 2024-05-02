# Application de gestion de tournois d'échec

## À propos

Formation OpenClassRooms - Developpeur d'application python - Projet 4

Développez un programme logiciel en Python (POO + design pattern MVC)


## Prérequis

Python >=3.12.0

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
- [flake8](https://flake8.pycqa.org/en/latest/) et [flake8-html](https://pypi.org/project/flake8-html/) pour le controle du livrable et la génération d'un rapport


## Documentation

### Table des matières

**Utilisation de l'application**
  - [Création des joueurs](#players)
  - [Création des tournois](#tournaments)
  - [Affichage des rapports](#reports)

**Organisation du livrable**
  - [fichier config.ini](#init)
  - [fichier chess.log](#logger)
  - [données JSON](#datastructure)
  - [Rapport flake8](#flake8)


### Utilisation de l'application

#### Création des joueurs

Le menu création de joueurs contient les catégories ci-dessous :

* *1. Afficher joueurs* : affiche la liste des joueurs et leurs ID.
* *2. Créer joueur* : saisie des informations pour la création d'un nouveau joueur.
* *3. Générer des joueurs (POUR TEST)* : génère aléatoirement des joueurs fictifs **POUR TEST UNIQUEMENT**


#### Création des tournois

Le menu création de tournois contient les catégories ci-dessous :

* *1. Afficher liste tournois* : affiche la liste des tournois et leurs ID
* *2. Créer tournoi* : saisie des informations pour la création d'un nouveau tournoi.
* *3. Générer des tournois (POUR TEST)* : génère aléatoirement des tournois fictifs **POUR TEST UNIQUEMENT**
* *4. Ajouter des joueurs à un tournoi* : Avant le début d'un tournoi, il faut ajouter les participants. Cette fonctionnalité n'est plus accessible une fois le tournoi commencé.
* *5. Commencer un tournoi* : Pour commencer un tournoi, celui ci doit avoir un nombre minimum de joueurs. Génère le 1er tour (avec la liste des matchs).
* *6. Ajouter le score d'un tour* : Saisie des scores d'un tour.
* *7. Débuter un nouveau tour* : les scores doivent avoir été ajoutés dans le tour précédent. Ce dernier est alors cloturé et un nouveau tour généré (avec la liste des matchs).
* *8. Terminer un tournoi* : Une fois l'ensemble des tours joués, permet de cloturer un tournoi.


#### Affichage des rapports

Les rapports sont accessibles depuis le menu principal > Rapports.
3 types de rapports sont consultables :
* liste de tous les joueurs par ordre alphabétique
* liste de tous les tournois
* pour un tournoi donné :
  - nom et dates du tournoi 
  - liste des joueurs du tournoi par ordre alphabétique
  - liste de tous les tours du tournoi et de tous les matchs du tour

#### fichier config.ini

Ce fichier contient l'emplacement du stockage des fichiers JSON

#### fichier chess.log

Un fichier chess.log est généré lors de l'utilisation de l'application.
Le log est paramétré par défaut au niveau "DEBUG".

#### données JSON

Deux fichiers JSON sont générés dans le repertoire .\data\
* players.json
* tournaments.json
Ils contiennent l'ensemble des données traitées par l'application.
Les données sont enregistrées en continu.
Elles sont automatiquement chargées à l'ouverture de l'application.

#### Rapport flake8

Un rapport avec flake8-html a été généré.
Celui ci est disponible dans le répertoire .\flake8_rapport\ du dépot.
Il a été généré avec la commande :
```bash
flake8 --format=html --htmldir=flake8_rapport --exclude env --max-line-length=119
```

## Gestion des versions

La dénomination des versions suit la spécification décrite par la [Gestion sémantique de version](https://semver.org/lang/fr/)

Les versions disponibles ainsi que les journaux décrivant les changements apportés sont disponibles depuis [la section releases](https://github.com/Mothraa/OCR_projet4/releases)

## Licence

Voir le fichier [LICENSE](./LICENSE.md) du dépôt.