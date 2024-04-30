from datetime import date


class MainMenuCommand:
    choice = None
    NB_CHOIX_MAX = 4

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer un choix")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 1 or int(self.choice) > self.NB_CHOIX_MAX:
            raise ValueError(f"Merci d'indiquer un nombre entre 1 et {self.NB_CHOIX_MAX}")

    def clean_up(self):
        self.choice = int(self.choice)


class PlayerMenuCommand:
    choice = None
    NB_CHOIX_MAX = 4

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
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
        self.id = None  # ID généré par le modèle
        self.national_chess_id = kwargs.get("national_chess_id")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.birthdate = kwargs.get("birthdate")
        self.self_validate()
        self.clean_up()

    def clean_up(self):
        self.birthdate = date.fromisoformat(self.birthdate)

    def self_validate(self):
        if not self.first_name:
            raise ValueError("Merci d'indiquer un nom")
        if not self.last_name:
            raise ValueError("Merci d'indiquer un prénom")
        if not self.birthdate:
            raise ValueError("Merci d'indiquer une date")

    def to_dict(self):
        return {
            "national_chess_id": self.national_chess_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate,
        }


class PlayerGenerateCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class TournamentMenuCommand:
    choice = None
    NB_CHOIX_MAX = 10

    def __init__(self, choice):
        self.choice = choice

        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer un choix")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 1 or int(self.choice) > self.NB_CHOIX_MAX:
            raise ValueError(f"Merci d'indiquer un nombre entre 1 et {self.NB_CHOIX_MAX}")

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
        if not self.name:
            raise ValueError("Merci d'indiquer un nom de tournoi")
        elif not self.location:
            raise ValueError("Merci d'indiquer un lieu de tournoi")
        elif (self.start_date is None) or (type(date.fromisoformat(self.start_date)) is not date):
            raise ValueError("Merci d'indiquer une date au format AAAA-MM-JJ")
        elif (self.end_date is None) or (type(date.fromisoformat(self.end_date)) is not date):
            raise ValueError("Merci d'indiquer une date au format AAAA-MM-JJ")
        elif self.number_of_rounds == "":
            self.number_of_rounds = self.DEFAULT_ROUND_NUMBER
        elif not self.number_of_rounds.isdigit():
            raise ValueError("Merci d'indiquer un nombre de tours")
        elif int(self.number_of_rounds) <= 0:
            raise ValueError("Le nombre de tours doit être un entier positif")

    def clean_up(self):
        self.start_date = date.fromisoformat(self.start_date)
        self.end_date = date.fromisoformat(self.end_date)
        self.number_of_rounds = int(self.number_of_rounds)

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description,
        }


class TournamentGenerateCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class TournamentAddPlayerCommand:
    tournament_id = None
    players_ids_string = None
    players_id_list = []

    def __init__(self, tournament_id, players_ids_string):
        self.tournament_id = tournament_id
        self.players_ids_string = players_ids_string
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.tournament_id:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.tournament_id), int) or int(self.tournament_id) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")
        # on sépare la chaine de caractère
        id_list = self.players_ids_string.strip().split(sep=" ")
        # on transforme chaque ID en int
        id_list = [int(player_id) for player_id in id_list]

    def clean_up(self):
        self.tournament_id = int(self.tournament_id)
        id_list = self.players_ids_string.strip().split(sep=" ")
        self.players_id_list = [int(player_id) for player_id in id_list]


class TournamentStartCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class TournamentEndCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer un nombre")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class CreateRoundCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class TournamentAddScoreCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)


class RoundAddScoreCommand:
    new_score1 = None
    new_score2 = None
    chess_match = None

    def __init__(self, new_score1, new_score2, chess_match):
        self.new_score1 = new_score1
        self.new_score2 = new_score2
        self.chess_match = chess_match

        self.self_validate()
        self.clean_up()
        self.update_score()

    def self_validate(self):
        if not self.new_score1:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(float(self.new_score1), float) or float(self.new_score1) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")
        elif not self.new_score2:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(float(self.new_score2), float) or float(self.new_score2) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.new_score1 = float(self.new_score1)
        self.new_score2 = float(self.new_score2)

    def update_score(self):
        (player1, _), (player2, _) = self.chess_match
        self.chess_match = (player1, self.new_score1), (player2, self.new_score2)


class ReportMenuCommand:
    choice = None
    NB_CHOIX_MAX = 4

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer un choix")
        try:
            choice_int = int(self.choice)
            if not (1 <= choice_int <= self.NB_CHOICES_MAX):
                raise ValueError(f"Merci d'indiquer un nombre entre 1 et {self.NB_CHOICES_MAX}")
        except ValueError:
            raise ValueError(f"Merci d'indiquer un nombre entre 1 et {self.NB_CHOICES_MAX}")

    def clean_up(self):
        self.choice = int(self.choice)


class ReportTournamentDetailsCommand:
    choice = None

    def __init__(self, choice):
        self.choice = choice
        self.self_validate()
        self.clean_up()

    def self_validate(self):
        if not self.choice:
            raise ValueError("Merci d'indiquer une valeur valide")
        elif not isinstance(int(self.choice), int) or int(self.choice) < 0:
            raise ValueError("Merci d'indiquer un nombre entier positif")

    def clean_up(self):
        self.choice = int(self.choice)
