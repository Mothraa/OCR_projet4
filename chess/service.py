import random
import json
from datetime import date, timedelta

from faker import Faker
from chess import model

from chess.utils import TournamentStatus
from chess.model import Player, Tournament

class Generator:
    def __init__(self) -> None:
        self.fake = Faker(locale="fr_FR")


class GeneratePlayerService(Generator):
    # on récupère la structure du joueur
    # TODO : passer par des dataclass https://docs.python.org/fr/3/tutorial/classes.html
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
        NB_ROUND_MIN = 2
        NB_ROUND_MAX = 6

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

                    if self.already_played_with_in_tournament(player1[0], player2[0], tournament):
                        i += 1
                    else:
                        player2 = temp_round_list.pop(i)
                        break
                # si il ne reste plus qu'un joueur sur la liste, pas le choix
                if len(temp_round_list) == 1:
                    player2 = temp_round_list.pop(0)
            matchs_list.append((player1, player2))

        return matchs_list

    def already_played_with_in_tournament(self, player1, player2, tournament) -> bool:
        """return True if already played with another player"""
        matchs_list = player1.get_matchs_history_by_tournament(tournament)
        flag = False
        for match in matchs_list:
            if match[2] == player2.id:
                flag = True
        return flag


class ReportService():

    @staticmethod
    def sort_players_list_by_name(player_list):
        player_list_sorted = sorted(player_list,  key=lambda player: player.last_name)
        return player_list_sorted


class JsonService():

    JSON_INDENT = 4
    PLAYERS_FILE_PATH = ".//data//players.json"
    # TOURNAMENTS_REPERTORY_PATH = ".//data//tournaments"
    TOURNAMENTS_FILE_PATH = ".//data//tournaments.json"

    def __init__(self):
        pass

    @staticmethod
    def load_data_from_json(json_file_path):
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data

    @staticmethod
    def save_data_to_json(data, json_file_path):
        with open(json_file_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=JsonService.JSON_INDENT)
            #lambda x: x.value

    @classmethod
    def add_player_as_json(cls, player: Player):

        player_dict = cls.convert_player_to_dict(player)
        data = cls.load_data_from_json(cls.PLAYERS_FILE_PATH)

        # Vérifier si les données à ajouter sont déjà présentes
        for item in data:
            # dans le cas ou le joueur est déjà présent
            if all(item[key] == player_dict[key] for key in player_dict):
                return
            # dans le cas de deux joueurs avec le même ID (mais des attributs différents)
            if item['id'] == player_dict['id']:
                print("Un joueur avec le même ID existe déjà.")
                return

        data.append(player_dict)
        cls.save_data_to_json(data, cls.PLAYERS_FILE_PATH)

    @classmethod
    def add_tournament_as_json(cls, tournament: Tournament):

        tournament_dict = cls.convert_tournament_to_dict(tournament)
        data = cls.load_data_from_json(cls.TOURNAMENTS_FILE_PATH)

        # Vérifier si les données à ajouter sont déjà présentes
        for item in data:
            # dans le cas ou le joueur est déjà présent
            if all(item[key] == tournament_dict[key] for key in tournament_dict):
                return
            # dans le cas de deux joueurs avec le même ID (mais des attributs différents)
            if item['id'] == tournament_dict['id']:
                print("Un tournoi avec le même ID existe déjà.")
                return

        data.append(tournament_dict)
        cls.save_data_to_json(data, cls.TOURNAMENTS_FILE_PATH)

    @classmethod
    def update_player_as_json(cls, player_to_update):
        pass

    @classmethod
    def update_tournament_as_json(cls, tournament_to_update):
        pass

    def get_players_from_json(self):
        pass

    def get_tournaments_from_json(self):
        pass

    @staticmethod
    def convert_attr_to_str(obj):
        if isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, TournamentStatus):
            return obj.name
        else:
            return obj

    # Conversion de l'objet Player en dictionnaire récursivement pour les listes imbriquées
    @classmethod
    def convert_player_to_dict(cls, obj):
        if isinstance(obj, Player):
            return {key: cls.convert_attr_to_str(value) for key, value in obj.__dict__.items()
                    if key != "players_repertory"}
        elif isinstance(obj, list):
            return [cls.convert_player_to_dict(item) for item in obj]
        else:
            return obj

    # Conversion de l'objet Player en dictionnaire récursivement pour les listes imbriquées
    @classmethod
    def convert_tournament_to_dict(cls, obj):
        if isinstance(obj, Tournament):
            return {key: cls.convert_attr_to_str(value) for key, value in obj.__dict__.items()
                    if key != "tournaments_repertory"}
        elif isinstance(obj, list):
            return [cls.convert_tournament_to_dict(item) for item in obj]
        else:
            return obj
        
    def load_json(self):
        # Mappage du statut pour le remettre de type enum
        for item in data:
            item["status"] = TournamentStatus[item["status"]]
        pass
