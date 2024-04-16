from datetime import date

from chess.model import Player, Tournament, TournamentStatus


class MainMenuCommand:
    choice = None
    NB_CHOIX_MAX = 4

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer un choix")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 1 or int(self.choice) > self.NB_CHOIX_MAX:
            raise ValueError(f"Merci d'indiquer un nombre entre 1 et {self.NB_CHOIX_MAX}")

    def clean_up(self):
        self.choice = int(self.choice)


class PlayerMenuCommand:
    choice = None
    NB_CHOIX_MAX = 4

    def __init__(self, choice):
        # faire hériter de MainMenuCommand ?
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer un choix")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 1 or int(self.choice) > self.NB_CHOIX_MAX:
            raise ValueError(f"Merci d'indiquer un nombre entre 1 et {self.NB_CHOIX_MAX}")

    def clean_up(self):
        self.choice = int(self.choice)


class PlayerCreateCommand:
    id = None
    national_chess_id = None
    first_name = None
    last_name = None
    birthdate = None

    def __init__(self, **kwargs):
        # self.national_chess_id = kwargs.get("national_chess_id")
        self.id = None # généré par le modèle
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.birthdate = kwargs.get("birthdate")

        self.self_validate()
        self.clean_up()
        self.to_dict()

    def self_validate(self):
        if self.first_name is None:
            raise ValueError("Merci d'indiquer un nom")
        if self.last_name is None:
            raise ValueError("Merci d'indiquer un prénom")
        if (self.birthdate is None) or (type(date.fromisoformat(self.birthdate)) is not date):
            raise ValueError("Merci d'indiquer une date au format AAAA-MM-JJ")

    def clean_up(self):
        self.birthdate = date.fromisoformat(self.birthdate)
    
    # TODO retourner également un dict pour les tournois
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate
        }


class PlayerGenerateCommand:
    choice = None

    def __init__(self, choice):
        # faire hériter de MainMenuCommand ?
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class TournamentMenuCommand:
    choice = None
    NB_CHOIX_MAX = 10

    def __init__(self, choice):
        # faire hériter de MainMenuCommand ?
        self.choice = choice

        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer un choix")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 1 or int(self.choice) > self.NB_CHOIX_MAX:
            raise ValueError(f"Merci d'indiquer un nombre entre 1 et {self.NB_CHOIX_MAX}")

    def clean_up(self):
        self.choice = int(self.choice)


class TournamentDetailCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class TournamentCreateCommand:
    DEFAULT_ROUND_NUMBER = 4
    id = None
    name = None
    location = None
    start_date = None
    end_date = None
    number_of_rounds = None
    description = None

    def __init__(self, **kwargs):
        self.id = None  # généré par le modèle
        self.name = kwargs.get("name")
        self.location = kwargs.get("location")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.number_of_rounds = kwargs.get("number_of_rounds")
        self.description = kwargs.get("description")

        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.name is None:
            raise ValueError("Merci d'indiquer un nom de tournoi")
        elif self.location is None:
            raise ValueError("Merci d'indiquer un lieu de tournoi")
        elif (self.start_date is None) or (type(date.fromisoformat(self.start_date)) is not date):
            raise ValueError("Merci d'indiquer une date au format AAAA-MM-JJ")
        elif (self.end_date is None) or (type(date.fromisoformat(self.end_date)) is not date):
            raise ValueError("Merci d'indiquer une date au format AAAA-MM-JJ")
        elif self.number_of_rounds == "":
            self.number_of_rounds = self.DEFAULT_ROUND_NUMBER
        elif type(self.number_of_rounds) is not int:
            raise ValueError("Merci d'indiquer un nombre de tours")

    def clean_up(self):
        self.start_date = date.fromisoformat(self.start_date)
        self.end_date = date.fromisoformat(self.end_date)
        self.number_of_rounds = int(self.number_of_rounds)


class TournamentGenerateCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class TournamentAddPlayerCommand:
    tournament_id = None
    players_id_list = []

    def __init__(self, tournament_id, input_players_list):
        self.tournament_id = tournament_id
        self.input_players_list = input_players_list
        self.self_validate()
        self.clean_up()
        self.check_tournament_status()

    def self_validate(self):
        if self.tournament_id is None:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.tournament_id), int) or int(self.tournament_id) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")
        # TODO vérifier si l'id renvoi bien vers un tournoi

        # on sépare la chaine de caractère
        id_list = self.input_players_list.strip().split(sep=" ")
        # on transforme chaque ID en int
        id_list = [int(player_id) for player_id in id_list]
        # on vérifie qui les ID indiqués existent
        if not [Player.find_by_id(player_id) for player_id in id_list]:
            raise ValueError("Merci d'indiquer des ID joueur valides")

    def clean_up(self):
        self.tournament_id = int(self.tournament_id)

        id_list = self.input_players_list.strip().split(sep=" ")
        self.players_id_list = [int(player_id) for player_id in id_list]

    def check_tournament_status(self):
        tournament = Tournament.find_by_id(self.tournament_id)
        # on vérifie que le statut du tournoi soit au statut CREATED
        if tournament.get_status() is not TournamentStatus.CREATED:
            raise ValueError(f"Impossible d'ajouter des joueurs, son statut est {tournament.status}")


class TournamentStartCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()
        self.check_tournament_status()

    def self_validate(self):

        if self.choice is None:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)

    def check_tournament_status(self):
        tournament = Tournament.find_by_id(self.choice)
        # on vérifie que le statut du tournoi soit au statut CREATED
        if tournament.get_status() is not TournamentStatus.CREATED:
            raise ValueError(f"Le tournoi ne peut être commencé, son statut est {tournament.get_status()}")

        # qu'il y ai au moins 2 joueurs
        if len(tournament.get_player_list()) <= 2:
            raise ValueError("Le tournoi ne peut être commencé, pas assez de joueurs")


class TournamentEndCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()
        self.check_tournament_status()
        self.check_played_matchs()

    def self_validate(self):

        if self.choice is None:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)

    def check_tournament_status(self):
        tournament = Tournament.find_by_id(self.choice)
        # on vérifie que le statut du tournoi soit au statut IN PROGRESS
        if tournament.get_status() is not TournamentStatus.IN_PROGRESS:
            raise ValueError(f"Le tournoi ne peut être terminé, son statut est {tournament.get_status()}")

        # que l'on est au dernier round
        if tournament.current_round_number != tournament.number_of_rounds:
            raise ValueError("Tous les tours du tournoi n'ont pas été joués")

    def check_played_matchs(self):
        tournament = Tournament.find_by_id(self.choice)
        # on vérifie que tous les matchs du dernier round ont été joués
        round_indice = tournament.get_current_round_number() - 1
        round = tournament.rounds_list[round_indice]
        for match in round.matchs_list:
            # on regarde les scores des matchs (sous la forme de tuples : (player1, score1)(player2, score2))
            # TODO créer une fonction get_match_score (par ex)
            if match[0][1] == 0.0 and match[1][1] == 0.0:
                raise ValueError("Les matchs du tournoi / tour indiqué ne sont pas terminés")


class CreateRoundCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()
        self.check_tournament_status()
        self.check_played_matchs()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)

    def check_tournament_status(self):
        tournament = Tournament.find_by_id(self.choice)
        # on vérifie que le statut du tournoi soit au statut IN_PROGRESS
        if tournament.get_status() is not TournamentStatus.IN_PROGRESS:
            raise ValueError(f"Le tournoi ne peut être poursuivi, son statut est {tournament.get_status()}")

        # on vérifie si on peut toujours ajouter des rounds (limite de rounds atteinte)
        if tournament.current_round_number == tournament.number_of_rounds:
            raise ValueError("Tous les tours du tournoi ont déjà été créés")

    def check_played_matchs(self):
        tournament = Tournament.find_by_id(self.choice)
        # on vérifie que tous les matchs du tour précédent ont été joués
        round_indice = tournament.get_current_round_number() - 1
        round = tournament.rounds_list[round_indice]
        for match in round.matchs_list:
            # on regarde les scores des matchs (sous la forme de tuples : (player1, score1)(player2, score2))
            # TODO créer une fonction get_match_score (par ex)
            if match[0][1] == 0.0 and match[1][1] == 0.0:
                raise ValueError("Les matchs du tournoi / tour indiqué ne sont pas terminés")


class TournamentIdCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()
        self.check_not_played_matchs()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)

    def check_not_played_matchs(self):
        tournament = Tournament.find_by_id(self.choice)
        # on vérifie que les matchs du tour n'ont pas été joués
        round = tournament.get_current_round()
        for match in round.matchs_list:
            # on regarde les scores des matchs (sous la forme de tuples : (player1, score1)(player2, score2))
            # TODO créer une fonction get_match_score (par ex)
            if match[0][1] != 0.0 and match[1][1] != 0.0:
                raise ValueError("Les matchs du tournoi / tour indiqué ont déjà été joués")


class RoundAddScore:
    new_score1 = None
    new_score2 = None
    match = None

    def __init__(self, new_score1, new_score2, match):
        self.new_score1 = new_score1
        self.new_score2 = new_score2
        self.match = match

        self.self_validate()
        self.clean_up()
        self.update_score()

    def self_validate(self):
        if self.new_score1 is None:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(float(self.new_score1), float) or float(self.new_score1) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")
        # TODO : ajouter la condition différent de 0.0, 0.5, 1.0
        if self.new_score2 is None:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(float(self.new_score2), float) or float(self.new_score2) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")
        # TODO : ajouter la condition différent de 0.0, 0.5, 1.0

        # TODO : le score ne peut etre que 0-1 ou 0.5-0.5 ou 1-0

    def clean_up(self):
        self.new_score1 = float(self.new_score1)
        self.new_score2 = float(self.new_score2)

    def update_score(self):
        (player1, score1), (player2, score2) = self.match
        self.match = (player1, self.new_score1), (player2, self.new_score2)


class ReportMenuCommand:
    choice = None
    NB_CHOIX_MAX = 4

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.choice is None:
            raise ValueError("Merci d'indiquer un choix")
        # TODO tester range(1, NB_CHOIX_MAX)
        elif not isinstance(int(self.choice), int) or int(self.choice) < 1 or int(self.choice) > self.NB_CHOIX_MAX:
            raise ValueError(f"Merci d'indiquer un nombre entre 1 et {self.NB_CHOIX_MAX}")

    def clean_up(self):
        self.choice = int(self.choice)
# exemple avec decorateur
    # def validate_input(func):
    #     def wrapper(self, *args, **kwargs):
    #         value = func(self, *args, **kwargs)
    #         if not value:
    #             raise ValueError(f"Merci d'indiquer {func.__doc__}.")
    #         return value
    #     return wrapper

    # logging.debug("choix menu >> " + str(args[choix - 1]))

    # @validate_input
    # def validate_first_name(self):
    #     """un prénom"""
    #     return self.first_name

    # @validate_input
    # def validate_last_name(self):
    #     """un nom"""
    #     return self.last_name
