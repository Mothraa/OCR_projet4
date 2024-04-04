from enum import Enum

class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class MainOption(ExtendedEnum):
    PLAYER_MENU_OPTION = 1
    TOURNAMENT_MENU_OPTION = 2
    CLOSE_PROGRAM_OPTION = 3


MAIN_MENU = """
    Application d'échec\n
    Menu principal\n
    1. Gestion joueurs
    2. Gestion Tournois
    3. Quitter
"""

PLAYER_MENU = """
    Menu joueurs\n
    1. Afficher joueurs
    2. Créer joueur
    3. Générer des joueurs (POUR TEST)
    4. Retour au menu principal
"""

PLAYER_CREATE_MENU = "**** Création d'un nouveau joueur ****"

PLAYER_GENERATE_MENU = """
    **** Génération aléatoire de joueurs ****\n
    Indiquer un nombre de joueurs à créer :
    """

TOURNAMENT_MENU = """
    Menu Tournois\n
    1. Afficher tournois
    2. Créer tournoi
    3. Générer des tournois (POUR TEST)
    4. Commencer un tournoi
    5. Poursuivre un tournoi
    6. Retour au menu principal
"""

TOURNAMENT_CREATE_MENU = "**** Création d'un nouveau tournoi ****"

ROUND_MENU = """
  Tours\n
  1. Ajouter un tour
  2. Générer un tour
"""
