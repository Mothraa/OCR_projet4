import random

from datetime import timedelta

from faker import Faker
from . import model
#from chess.controller import PlayerController

class Generator:
    def __init__(self) -> None:
        self.fake = Faker(locale="fr_FR")


class GeneratePlayerService(Generator):
    # on récupère la structure du joueur
    player_attrs = model.Player

    def __init__(self) -> None:
        super().__init__()

    def generate_player_all_attrs(self):

        self.player_attrs.first_name = self.fake.unique.first_name()
        self.player_attrs.last_name = self.fake.unique.last_name()
        self.player_attrs.birthdate = self.fake.unique.date_of_birth(minimum_age=6, maximum_age=99)
        self.player_attrs.national_chess_id = self.fake.unique.bothify(text="??%%%%%").upper()

        return self.player_attrs


class GenerateTournamentService(Generator):
    # on récupère la structure de tournoi
    tournament_attrs = model.Tournament

    def __init__(self) -> None:
        super().__init__()

    def generate_tournament_all_attrs(self):

        DELTA_DATE = 3  # nombre de jours max entre début et fin d'un tournoi
        NB_ROUND_MIN = 4
        NB_ROUND_MAX = 8

        location = self.fake.unique.city()
        date_debut = self.fake.unique.date_this_year(before_today=False, after_today=True)
        date_fin_max = date_debut + timedelta(days=DELTA_DATE)
        date_fin = self.fake.date_time_between(start_date=date_debut, end_date=date_fin_max)

        self.tournament_attrs.name = "Tournoi de {}".format(location)
        self.tournament_attrs.location = location
        self.tournament_attrs.start_date = date_debut
        self.tournament_attrs.end_date = date_fin
        self.tournament_attrs.number_of_rounds = random.randint(NB_ROUND_MIN, NB_ROUND_MAX)
        self.tournament_attrs.description = "Organisé par {}".format(self.fake.unique.name_nonbinary())

        return self.tournament_attrs


# Service: Approche 2
# class GenerateRoundService(Generator):
#     def __init__(self) -> None:
#         super().__init__()
    
#     def create_round(self, tournament: Tournament, players: Player[]) -> None:
#         tournament = Tournament.find_by_code(command.getTournamentCode())
#         players = Player.find_by_tournaments(tournament)
#         games = self.compose_games(tournament, players)
#         return Round.create(tournament, games)

#     def compose_games(tournament, playes):
#         match = ()
#         # TODO: Logique composer les matchs. (P1, P2, 0, 0
#         return match


class CreatorDeprecated(Generator):
    def __init__(self) -> None:
        super().__init__()

    def round(self):
        pass

    def match(self):
        pass

    @staticmethod
    def score(player1, player2):
        # scores randomisés et pondérés
        tirage = random.choices(['first', 'second', 'equal'], weights=(35, 35, 25))[0]
        if tirage == 'equal':
            score_player1 = 0.5
            score_player2 = 0.5
        elif tirage == 'first':
            score_player1 = 1
            score_player2 = 0
        elif tirage == 'second':
            score_player1 = 0
            score_player2 = 1

        return ([player1, score_player1], [player2, score_player2])


#     creator = Creator()
#     toto = creator.player(3)
#     player_liste = Player.get_player_repertory()

class SaveAsJSON:
    def __init__(self):
        pass
# #     print(toto)
# #     print(type(toto))
# #     save = SaveAsJSON()
# #     save.player(toto)

class ReadFromJSON:
    def __init__(self):
        pass