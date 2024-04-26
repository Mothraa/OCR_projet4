# MAIN

MAIN_MENU = """
    **** Application d'échec ****\n
    Menu principal\n
    1. Gestion joueurs
    2. Gestion Tournois
    3. Rapports
    4. Quitter
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
    2. Créer tournoi
    3. Générer des tournois (POUR TEST)
    4. Ajouter des joueurs à un tournoi
    5. Commencer un tournoi
    6. Ajouter le score d'un tour
    7. Débuter un nouveau tour
    8. Terminer un tournoi
    9. Retour au menu principal
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

# ROUNDS

ROUND_MENU = """**** Ajouter un tour à un tournoi ****\n
    << Attention >> l'ajout d'un tour va cloturer le tour précédent.
    Indiquez l'ID du tournoi auquel vous souhaitez ajouter un tour :
    """

ROUND_MENU_ADD_SCORES = """**** Ajouter des scores à un tour ****\n
    Indiquez l'ID du tournoi auquel vous souhaitez ajouter les scores :
    """

TOURNAMENT_END_MENU = """**** Terminer un tournoi ****\n
    << Attention >> Tous les tours doivent être terminés pour terminer un tournoi
    Indiquer l'ID du tournoi :
    """

# REPORT

REPORT_MENU = """
    Menu rapports\n
    1. liste de tous les joueurs par ordre alphabétique
    2. liste de tous les tournois
    3. détails d'un tournoi
    4. Retour au menu principal
"""

REPORT_TOURNAMENT_DETAILS = """**** Détails d'un tournoi ****\n
    Indiquez l'ID du tournoi :
    """
