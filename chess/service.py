import random

from datetime import datetime, timedelta

from faker import Faker
from chess import model
# from chess.controller import PlayerController


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
        date_fin = self.fake.date_between(start_date=date_debut, end_date=date_fin_max)

        self.tournament_attrs.name = "Tournoi de {}".format(location)
        self.tournament_attrs.location = location
        self.tournament_attrs.start_date = date_debut
        self.tournament_attrs.end_date = date_fin
        self.tournament_attrs.number_of_rounds = random.randint(NB_ROUND_MIN, NB_ROUND_MAX)
        self.tournament_attrs.description = "Organisé par {}".format(self.fake.unique.name_nonbinary())

        return self.tournament_attrs


# Service: Approche 2
class GenerateRoundService(Generator):
    round_attrs = model.Round

    def __init__(self) -> None:
        super().__init__()

    def create_matchs(self, tournament: model.Tournament):
        INIT_SCORE = 0.0
        round_number = tournament.get_current_round_number()
        tournament.sort_players_by_score()
        temp_round_list = tournament.player_list.copy()
        # remise à 0 des scores pour le nouveau round
        for i, (_, _) in enumerate(temp_round_list):
            player = temp_round_list[i][0]
            temp_round_list[i] = (player, INIT_SCORE)

        matchs_list = []
        # score_player1 = None
        # score_player2 = None

        while len(temp_round_list) >= 2:
            # au premier tour random sur les paires
            if round_number == 0:  # le premier round est celui d'indice 0
                player1 = temp_round_list.pop(random.randrange(len(temp_round_list)))
                player2 = temp_round_list.pop(random.randrange(len(temp_round_list)))
            else:
                # ensuite on prend suivant l'ordre du classement
                player1 = temp_round_list.pop(0)
                i = 0
                # On évite de créer des matchs identiques
                while len(temp_round_list) > 1:
                    # on regarde si le player1 a déjà joué avec le player2, si oui on passe au suivant
                    # TODO : précision sur le cahier des charges, se limiter aux joueurs ayant le même score ?

                    player2 = temp_round_list[i]

                    if player1[0].already_played_with_in_tournament(player2[0], tournament):
                        i += 1
                    else:
                        player2 = temp_round_list.pop(i)
                        break
                # si il ne reste plus qu'un joueur sur la liste, pas le choix
                if len(temp_round_list) == 1:
                    player2 = temp_round_list.pop(0)
            matchs_list.append((player1, player2))

        return matchs_list


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
