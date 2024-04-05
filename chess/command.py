from datetime import date

from chess.model import Player, Tournament, TournamentStatus

# TODO : a dispatch dans les classes des commands
class InputManagement():
    def __init__():
        pass

    @staticmethod
    def check_dates(self, start_date, end_date):
        """vérification :
            - du format date
            - que la date de début est avant la date de fin
            - que les dates sont à venir
        """
        pass

    @staticmethod
    def check_chess_id(self):
        pass


class MainMenuCommand:
    choice = None
    NB_CHOIX_MAX = 3

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
    national_chess_id = None
    first_name = None
    last_name = None
    birthdate = None

    def __init__(self, **kwargs):
        # self.national_chess_id = kwargs.get("national_chess_id")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.birthdate = kwargs.get("birthdate")

        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if self.first_name is None:
            raise ValueError("Merci d'indiquer un nom")
        if self.last_name is None:
            raise ValueError("Merci d'indiquer un prénom")
        if (self.birthdate is None) or (type(date.fromisoformat(self.birthdate)) is not date):
            raise ValueError("Merci d'indiquer une date au format AAAA-MM-JJ")

    def clean_up(self):
        self.birthdate = date.fromisoformat(self.birthdate)


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
    NB_CHOIX_MAX = 8

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

    name = None
    location = None
    start_date = None
    end_date = None
    number_of_rounds = None
    description = None

    def __init__(self, **kwargs):
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
    """Commande qui attend l'ID d'un tournoi (en int)"""
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
        tournament = Tournament.get_tournament_from_id(self.choice)
        # on vérifie que le statut du tournoi soit au statut CREATED
        if tournament.get_status() is TournamentStatus.CREATED:
            raise ValueError(f"Le tournoi ne peut être commencé, son statut est {tournament.status}")


class PlayersToAddInTournamentCommand:
    players_id_list = []

    def __init__(self, input_players_list):
        self.input_players_list = input_players_list
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        # on sépare la chaine de caractère
        id_list = self.input_players_list.strip().split(sep=" ")
        # on transforme chaque ID en int
        id_list = [int(player_id) for player_id in id_list]
        # on vérifie qui les ID indiqués existent
        [Player.get_player_from_id(player_id) for player_id in id_list]

    def clean_up(self):
        id_list = self.input_players_list.strip().split(sep=" ")
        self.players_id_list = [int(player_id) for player_id in id_list]


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
        tournament = Tournament.get_tournament_from_id(self.choice)
        # on vérifie que le statut du tournoi soit au statut CREATED
        if tournament.get_status() != TournamentStatus.CREATED:
            raise ValueError(f"Le tournoi ne peut être commencé son statut est {tournament.status}")


# exemple avec decorateur
    # def validate_input(func):
    #     def wrapper(self, *args, **kwargs):
    #         value = func(self, *args, **kwargs)
    #         if not value:
    #             raise ValueError(f"Merci d'indiquer {func.__doc__}.")
    #         return value
    #     return wrapper

    # @validate_input
    # def validate_first_name(self):
    #     """un prénom"""
    #     return self.first_name

    # @validate_input
    # def validate_last_name(self):
    #     """un nom"""
    #     return self.last_name
