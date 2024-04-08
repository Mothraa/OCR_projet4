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

# PLAYERS

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
    Indiquer le nombre de joueurs à créer :
    """

# TOURNAMENTS

TOURNAMENT_MENU = """
    Menu Tournois\n
    1. Afficher liste tournois
    2. Afficher le détail d'un tournoi
    3. Créer tournoi
    4. Générer des tournois (POUR TEST)
    5. Ajouter des joueurs à un tournoi
    6. Commencer un tournoi
    7. Poursuivre un tournoi
    8. Retour au menu principal
"""

TOURNAMENT_DETAIL_MENU = """**** Détails sur un tournoi ****\n
    Indiquer l'ID du tournoi :
    """

TOURNAMENT_CREATE_MENU = "**** Création d'un nouveau tournoi ****"

TOURNAMENT_GENERATE_MENU = """
    **** Génération aléatoire de tournois ****\n
    Indiquer le nombre de tournois à créer :
    """

TOURNAMENT_ADD_PLAYERS_MENU = """
    **** Ajout de joueurs à un tournoi ****\n
    Indiquer l'ID du tournoi :
    """

TOURNAMENT_ADD_PLAYERS_LIST = """
    Indiquer la liste des ID des joueurs à ajouter (séparés par des espaces) :
    """

TOURNAMENT_START_MENU = """**** Débuter un tournoi ****\n
    << Attention >> vous ne pourrez plus ajouter de joueur une fois le tournoi commencé.
    Indiquer l'ID du tournoi :
    """

ROUND_MENU = """**** Ajouter un tour à un tournoi ****\n
    << Attention >> l'ajout d'un tour va cloturer le tour précédent.
    Indiquez l'ID du tournoi auquel vous souhaitez ajouter un tour :
    """
