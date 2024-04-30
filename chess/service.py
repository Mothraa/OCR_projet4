import random
import json
import os
import re
from datetime import date, datetime, timedelta

from faker import Faker

from chess.utils import TournamentStatus
from chess.model import Player, Tournament, ChessRound
from chess.exceptions import (
                            NationalChessIdFormatError,
                            InvalidDateFormatError,
                            TournamentStatusError,
                            )


class Generator:
    """initialisation of faker"""
    def __init__(self) -> None:
        self.fake = Faker(locale="fr_FR")


class GeneratePlayerService(Generator):
    """generate fake Player's data with module faker"""
    # TODO : passer par des dataclass ? https://docs.python.org/fr/3/tutorial/classes.html
    def __init__(self) -> None:
        super().__init__()

    def generate_player_all_attrs(self):
        first_name = self.fake.unique.first_name()
        last_name = self.fake.unique.last_name()
        # on transforme la date en datetime
        # birthdate = datetime.combine(self.fake.unique.date_of_birth(minimum_age=6, maximum_age=99), datetime.time())
        birthdate = self.fake.unique.date_of_birth(minimum_age=6, maximum_age=99)
        national_chess_id = self.fake.unique.bothify(text="??%%%%%").upper()

        player_data = {
            'first_name': first_name,
            'last_name': last_name,
            'birthdate': birthdate,
            'national_chess_id': national_chess_id
        }

        return player_data


class GenerateTournamentService(Generator):
    """generate fake Tournament's data with module faker"""
    def __init__(self) -> None:
        super().__init__()

    def generate_tournament_all_attrs(self):
        DELTA_DATE = 3  # nombre de jours max entre début et fin d'un tournoi
        NB_ROUND_MIN = 2
        NB_ROUND_MAX = 4

        location = self.fake.unique.city()
        name = "Tournoi de {}".format(location)
        date_debut = self.fake.unique.date_this_year(before_today=False, after_today=True)
        date_fin_max = date_debut + timedelta(days=DELTA_DATE)
        date_fin = self.fake.date_between(start_date=date_debut, end_date=date_fin_max)
        number_of_rounds = random.randint(NB_ROUND_MIN, NB_ROUND_MAX)
        description = "Organisé par {}".format(self.fake.unique.name_nonbinary())

        tournament_data = {
            'name': name,
            'location': location,
            'start_date': date_debut,
            'end_date': date_fin,
            'number_of_rounds': number_of_rounds,
            'description': description
        }
        return tournament_data


class RoundService:
    INIT_SCORE = 0.0

    def __init__(self) -> None:
        pass

    def create_matchs(self, tournament: Tournament):
        round_number = tournament.current_round_number
        tournament.sort_players_by_score()
        temp_round_list = tournament.player_score_list.copy()
        # remise à 0 des scores pour le nouveau round
        for i, (_, _) in enumerate(temp_round_list):
            player = temp_round_list[i][0]
            temp_round_list[i] = (player, self.INIT_SCORE)
        matchs_list = []

        while len(temp_round_list) >= 2:
            # au premier tour random sur les paires (player1, player2)
            if round_number == 1:
                player1 = temp_round_list.pop(random.randrange(len(temp_round_list)))
                player2 = temp_round_list.pop(random.randrange(len(temp_round_list)))
            else:
                # pour les rounds suivant on prend suivant l'ordre du classement
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
                # si il ne reste plus qu'un joueur sur la liste, on le récupère
                if len(temp_round_list) == 1:
                    player2 = temp_round_list.pop(0)
            matchs_list.append((player1, player2))
        return matchs_list

    def already_played_with_in_tournament(self, player1_id, player2_id, tournament) -> bool:
        """return True if already played with another player"""
        player1 = Player.find_by_id(player1_id)
        matchs_list = player1.matchs_history_by_tournament(tournament)
        for chess_match in matchs_list:
            if chess_match[2] == player2_id:
                return True
        return False

    @staticmethod
    def add_score_in_tournament_ranking(tournament: Tournament, score_to_add: float, player_id: int):
        player_list = tournament.player_score_list
        player_index = None
        for index, (p_id, _) in enumerate(player_list):
            if p_id == player_id:
                player_index = index
                break
        (_, score) = player_list[player_index]
        new_score = score + score_to_add
        tournament.player_score_list[player_index] = (player_id, new_score)
        # TODO : déplacer le set_player_list dans le controller une fois tous les scores modifiés pour limiter les maj
        # update player score list
        tournament.player_score_list = player_list

    @classmethod
    def add_scores_to_tournament(cls, tournament, view):
        # on récupère le tour courant (contenant la liste des matchs)
        current_round = tournament.current_round()
        new_matchs_list = []
        for chess_match in current_round.matchs_list:
            (player1_id, _), (player2_id, _) = chess_match
            player1 = Player.find_by_id(player1_id)
            player2 = Player.find_by_id(player2_id)
            # TODO regrouper player1, 2 dans match ?
            command = view(player1, player2, chess_match)
            (player1_id, score1), (player2_id, score2) = command.chess_match
            RoundAddScoreValidate.validate(score1, score2)

            cls.add_score_in_tournament_ranking(tournament, score1, player1_id)
            cls.add_score_in_tournament_ranking(tournament, score2, player2_id)
            PlayerService.set_history(player1, tournament, current_round, command.chess_match)
            PlayerService.set_history(player2, tournament, current_round, command.chess_match)
            # TODO : update json player1 et player2
            new_matchs_list.append(command.chess_match)
        # TODO : ajouter le score au classement du tournoi
        current_round.matchs_list = new_matchs_list


class ReportService:

    @staticmethod
    def sort_players_list_by_name(player_list):
        player_list_sorted = sorted(player_list,  key=lambda player: player.last_name)
        return player_list_sorted

    @staticmethod
    def tournament_details(tournament: Tournament):
        tournament_dict = TournamentService.convert_tournament_to_dict(tournament)
        # Converti la liste de joueurs du tournoi en une liste d'instances Player
        tournament_player_instances = [Player.find_by_id(player_id)
                                       for player_id, _ in tournament_dict['player_score_list']]
        # Trier les instances de joueur par nom
        player_list_sorted = ReportService.sort_players_list_by_name(tournament_player_instances)
        # Créer un dictionnaire pour mapper les ID de joueur à leurs noms
        player_names = {player.id: f"{player.first_name} {player.last_name}" for player in tournament_player_instances}
        # Mise à jour des noms des joueurs dans tournament_dict
        for i, player in enumerate(player_list_sorted):
            player_name = f"{player.first_name} {player.last_name}"
            tournament_dict['player_score_list'][i] = [player_name,
                                                       f"score: {tournament_dict['player_score_list'][i][1]}"]
        # Remplace l'ID par les noms des joueurs pour chaque match
        for tournament_round in tournament_dict['rounds_list']:
            updated_matchs_list = []  # Liste pour stocker les matchs mis à jour pour ce tournoi
            for chess_match in tournament_round['matchs_list']:
                player1_id, score_player1 = chess_match[0]
                player2_id, score_player2 = chess_match[1]
                player1_name = player_names.get(player1_id)
                player2_name = player_names.get(player2_id)
                updated_chess_match = [
                    (player1_name, score_player1),
                    (player2_name, score_player2)
                ]
                updated_matchs_list.append(updated_chess_match)
            tournament_round['matchs_list'] = updated_matchs_list
        return tournament_dict


class JsonService:

    JSON_INDENT = 4

    def __init__(self):
        pass

    def load_app_data(self):
        print("**** chargement des données depuis les fichiers json ****")
        players = PlayerService.load_players_from_json()
        print("Chargement de {} joueurs".format(len(players)))
        tournaments = TournamentService.load_tournaments_from_json()
        print("Chargement de {} tournois".format(len(tournaments)))

    @staticmethod
    def create_json_file(json_file_path):
        """Create a void JSON file if not exist"""
        if not os.path.exists(json_file_path):
            with open(json_file_path, "w") as f:
                json.dump([], f)

    @staticmethod
    def convert_attr_to_str(obj):
        """Convert attributs/objects into string for JSON serialisation"""
        if isinstance(obj, datetime):
            # return date format : '%Y-%m-%dT%H:%M:%S' (without millisecondes)
            return obj.isoformat(timespec="seconds")
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, TournamentStatus):
            return obj.name
        else:
            return obj

    @staticmethod
    def load_data_from_file(json_file_path):
        """load JSON data from file"""
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data

    @staticmethod
    def save_data_to_file(data, json_file_path):
        """save serialised JSON data into file"""
        with open(json_file_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=JsonService.JSON_INDENT)


class PlayerService:
    PLAYERS_FILE_PATH = None

    def __init__(self, players_file_path):
        PlayerService.PLAYERS_FILE_PATH = players_file_path

    @classmethod
    def player_exists(cls, data, player_dict) -> bool:
        """True if the player already exist in datas"""
        for item in data:
            if item['id'] == player_dict['id']:
                print("Un joueur avec le même ID existe déjà.")
                return True
        return False

    @classmethod
    def convert_player_to_dict(cls, obj):
        """Convert object Player to dict recursively (imbricated lists)"""
        if isinstance(obj, Player):
            return {key: cls.convert_player_to_dict(value) for key, value in obj.to_json().items()}
        elif isinstance(obj, list):
            return [cls.convert_player_to_dict(item) for item in obj]
        else:
            return JsonService.convert_attr_to_str(obj)

    # @classmethod
    # def convert_player_to_dict(cls, obj):
    #     """Convert object Player to dict recursively (imbricated lists)"""
    #     if isinstance(obj, Player):
    #         return {key: JsonService.convert_attr_to_str(value) for key, value in obj.__dict__.items()
    #                 if key != "_players_repertory"}
    #     elif isinstance(obj, list):
    #         return [cls.convert_player_to_dict(item) for item in obj]
    #     else:
    #         return obj

    @classmethod
    def add_player_as_json(cls, player: Player):
        """add a Player in the JSON file"""
        player_dict = cls.convert_player_to_dict(player)
        data = JsonService.load_data_from_file(cls.PLAYERS_FILE_PATH)
        # Vérifier si les données à ajouter sont déjà présentes dans le fichier json
        if not cls.player_exists(data, player_dict):
            data.append(player_dict)
            JsonService.save_data_to_file(data, cls.PLAYERS_FILE_PATH)

    @classmethod
    def update_player_as_json(cls, player: Player):
        """update an existing Player in the JSON file"""
        # TODO reprendre add_player_as_json et update_player_as_json pour optimiser le code
        player_dict = cls.convert_player_to_dict(player)
        data = JsonService.load_data_from_file(cls.PLAYERS_FILE_PATH)
        # mise à jour des données du joueur
        for item in data:
            if item['id'] == player_dict['id']:
                # Update player's data in the list
                item.update(player_dict)
                break
        # enregistrement des données en json
        JsonService.save_data_to_file(data, cls.PLAYERS_FILE_PATH)

    @classmethod
    def load_players_from_json(cls):
        """instantiation of Players from JSON data"""
        data = JsonService.load_data_from_file(cls.PLAYERS_FILE_PATH)
        players = []
        for player_data in data:
            # convert str to date
            if "birthdate" in player_data:
                player_data["birthdate"] = datetime.strptime(player_data["birthdate"], '%Y-%m-%d').date()
            # instancie les joueurs
            player = Player(**player_data)
            players.append(player)
        return players

    # @classmethod
    # def convert_player_to_dict(cls, obj):
    #     """Convert object Player to dict recursively (imbricated lists)"""
    #     if isinstance(obj, Player):
    #         return {key: JsonService.convert_attr_to_str(value) for key, value in obj.__dict__.items()
    #                 if key != "_players_repertory"}
    #     elif isinstance(obj, list):
    #         return [cls.convert_player_to_dict(item) for item in obj]
    #     else:
    #         return obj

    @staticmethod
    def set_history(player: Player, tournament: Tournament, round: ChessRound, chess_match):
        """Save a match in the player's match history"""
        (player1_id, score1), (player2_id, score2) = chess_match
        # on détermine si le joueur (player_id) est le player1 ou le player2
        player_id = player.id
        opponent_id = player2_id if player1_id is player_id else player1_id
        score_player = score1 if player1_id is player_id else score2
        score_opponent = score2 if player1_id is player_id else score1

        # format : liste de tuples => (ID tournoi, round, ID adversaire, score_joueur, score_adversaire)
        match_info = {
            "tournament_id": tournament.id,
            "round_id": round.id,
            "opponent_id": opponent_id,
            "score_player": score_player,
            "score_opponent": score_opponent
        }

        player.set_match_history(**match_info)


class TournamentService:
    TOURNAMENTS_FILE_PATH = None

    def __init__(self, tournaments_file_path):
        TournamentService.TOURNAMENTS_FILE_PATH = tournaments_file_path

    @classmethod
    def tournament_exists(cls, data, tournament_dict) -> bool:
        """True if the tournament already exist in datas"""
        for item in data:
            if item["id"] == tournament_dict["id"]:
                print("Un tournoi avec le même ID existe déjà.")
                return True
        return False

    @classmethod
    def add_tournament_as_json(cls, tournament: Tournament):
        """add a Tournament in the JSON file"""
        tournament_dict = cls.convert_tournament_to_dict(tournament)
        data = JsonService.load_data_from_file(cls.TOURNAMENTS_FILE_PATH)
        # On vérifie si les données à ajouter sont déjà présentes dans le fichier json
        # TODO : a reprendre avec l'update
        if not cls.tournament_exists(data, tournament_dict):
            data.append(tournament_dict)
            JsonService.save_data_to_file(data, cls.TOURNAMENTS_FILE_PATH)

    @classmethod
    def update_tournament_as_json(cls, tournament_to_update):
        """update an existing tournament in the JSON file"""
        tournament_dict = cls.convert_tournament_to_dict(tournament_to_update)
        data = JsonService.load_data_from_file(cls.TOURNAMENTS_FILE_PATH)
        # mise à jour des données du joueur
        for item in data:
            if item["id"] == tournament_dict["id"]:
                # Update player's data in the list
                item.update(tournament_dict)
                break
        # enregistrement des données en json
        JsonService.save_data_to_file(data, cls.TOURNAMENTS_FILE_PATH)

    @classmethod
    def load_tournaments_from_json(cls):
        """instantiation of Tournaments from JSON data"""
        data = JsonService.load_data_from_file(cls.TOURNAMENTS_FILE_PATH)
        tournaments = []
        for tournament_data in data:
            # convert str to date
            if "start_date" in tournament_data:
                tournament_data["start_date"] = datetime.strptime(tournament_data["start_date"], '%Y-%m-%d').date()
            elif "end_date" in tournament_data:
                tournament_data["end_date"] = datetime.strptime(tournament_data["end_date"], '%Y-%m-%d').date()
            round_list = []
            # load Rounds and convert str to date
            if "rounds_list" in tournament_data:
                for round_data in tournament_data["rounds_list"]:
                    if "start_date" in tournament_data:
                        round_data["start_date"] = datetime.strptime(round_data["start_date"], '%Y-%m-%dT%H:%M:%S')
                    elif "end_date" in tournament_data:
                        round_data["end_date"] = datetime.strptime(round_data["end_date"], '%Y-%m-%dT%H:%M:%S')
                    round_list.append(ChessRound(**round_data))
            tournament_data["rounds_list"] = round_list
            # load status as enum
            if "status" in tournament_data:
                # enum mapping
                status_enum = TournamentStatus[tournament_data["status"]]
                tournament_data["status"] = status_enum
            # tournament instantiation
            tournament = Tournament(**tournament_data)
            # add to the tournaments list
            tournaments.append(tournament)
        return tournaments

    @classmethod
    def convert_tournament_to_dict(cls, obj):
        """Convert object Tournament to dict recursively (imbricated lists)"""
        if isinstance(obj, Tournament):
            tournament_dict = {key: cls.convert_tournament_to_dict(value)
                               for key, value in obj.to_json().items()}
            # Conversion de la liste de rounds en dictionnaire
            if obj.rounds_list:
                tournament_dict['rounds_list'] = [
                    cls.convert_tournament_to_dict(round_item)
                    for round_item in obj.rounds_list
                    ]
            return tournament_dict
        elif isinstance(obj, ChessRound):
            round_dict = {key: cls.convert_tournament_to_dict(value)
                          for key, value in obj.to_json().items()}
            return round_dict
        elif isinstance(obj, list):
            return [cls.convert_tournament_to_dict(item) for item in obj]
        else:
            return JsonService.convert_attr_to_str(obj)

    @classmethod
    def convert_player_to_dict(cls, obj):
        """Convert object Player to dict recursively (imbricated lists)"""
        if isinstance(obj, Player):
            return {key: cls.convert_player_to_dict(value) for key, value in obj.to_json().items()}
        elif isinstance(obj, list):
            return [cls.convert_player_to_dict(item) for item in obj]
        else:
            return JsonService.convert_attr_to_str(obj)


class ValidateCommandService:

    @classmethod
    def validate_national_chess_id(cls, national_chess_id):
        """validate national_chess_id format. Expected : 2 uppercase letters + 5 numbers"""
        pattern = r'^[A-Z]{2}\d{5}$'
        if not bool(re.match(pattern, national_chess_id)):
            raise NationalChessIdFormatError()

    @classmethod
    def validate_date_format(cls, date_value: date):
        """validate date format"""
        # TODO : a améliorer, la conversion s'effectue dans la command
        if not isinstance(date_value, (date, datetime)):
            raise InvalidDateFormatError()

    @classmethod
    def validate_tournament_exists(self, tournament_id: int):
        """validate the ID refers to an existing tournament"""
        # TODO : validation a suppr, exception ajoutée à find_by_id
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            raise ValueError("Merci d'indiquer un numéro de tournoi existant")

    @classmethod
    def validate_player_exists(self, player_id: int):
        """validate the ID refers to an existing player"""
        # TODO : validation a suppr, exception ajoutée à find_by_id
        player = Player.find_by_id(player_id)
        if not player:
            raise ValueError("Merci d'indiquer un numéro de tournoi existant")

    @classmethod
    def validate_tournament_status(cls, tournament_id, expected_status: TournamentStatus):
        """validate if the tournament status matches the specified status"""
        tournament = Tournament.find_by_id(tournament_id)
        if tournament.status is not expected_status:
            raise TournamentStatusError(tournament.status)

    @classmethod
    def validate_already_added_players(cls, tournament_id: int, players_ids_to_add: list):
        """validate if the player has already been added to the tournament"""
        tournament = Tournament.find_by_id(tournament_id)
        # on recupère les ID des joueurs de la liste du tournoi
        existing_players_ids = [player[0] for player in tournament.player_score_list]
        # on regarde si il y a une correspondance entre les deux listes (players_ids_to_add et existing_players_ids)
        already_added_player_ids = [player_id for player_id in players_ids_to_add if player_id in existing_players_ids]
        # si c'est le cas, on lève une exception
        if already_added_player_ids:
            raise ValueError(f"Le(s) joueur(s) : {already_added_player_ids} a/ont déjà été ajouté(s) au tournoi")

    @classmethod
    def validate_minimum_players(cls, tournament_id: int):
        """Validate minimum of 2 players for starting a tournament"""
        tournament = Tournament.find_by_id(tournament_id)
        if len(tournament.player_score_list) <= 2:
            raise ValueError("Le tournoi ne peut être commencé, pas assez de joueurs")

    @classmethod
    def validate_last_round_reached(cls, tournament_id: int):
        """Check if we are in the last round"""
        tournament = Tournament.find_by_id(tournament_id)
        if tournament.current_round_number != tournament.number_of_rounds:
            raise ValueError("Tous les tours du tournoi n'ont pas été joués")

    @classmethod
    def validate_round_matches(cls, tournament_id: int, check_played=True):
        """Validate the completion status of matches in the current round
        Args:
            tournament_id : tournament's id
            check_played :
                True : check if matches have been played
                    (raises an exception if a match in the current round
                    has not been played)
                False : check if matches have not been played
                    (raises an exception if a match in the current round
                    has already been played)
        """
        tournament = Tournament.find_by_id(tournament_id)
        chess_round = tournament.current_round()
        for chess_match in chess_round.matchs_list:
            (_, score1), (_, score2) = chess_match
            if check_played:
                if score1 == 0.0 and score2 == 0.0:
                    raise ValueError(f"Les matchs du tour ({chess_round.round_name}) ne sont pas terminés")
            else:
                if score1 != 0.0 and score2 != 0.0:
                    raise ValueError(f"Les matchs du tour ({chess_round.round_name}) ont déjà été joués")

    @classmethod
    def validate_match_score(cls, score1: float, score2: float):
        """valid if the scores entered by the user are compliant with rules"""
        if float(score1) not in [0.0, 0.5, 1.0]:
            raise ValueError("Merci d'indiquer une valeur de 0, 0.5 ou 1 pour le joueur 1")
        elif float(score2) not in [0.0, 0.5, 1.0]:
            raise ValueError("Merci d'indiquer une valeur de 0, 0.5 ou 1 pour le joueur 2")
        elif score1 == 1.0 and score2 != 0.0:
            raise ValueError("Les scores doivent être soit 0-1, 0.5-0.5, ou 1-0")
        elif score1 == 0.0 and score2 != 1.0:
            raise ValueError("Les scores doivent être soit 0-1, 0.5-0.5, ou 1-0")
        elif score1 == 0.5 and score2 != 0.5:
            raise ValueError("Les scores doivent être soit 0-1, 0.5-0.5, ou 1-0")


class TournamentAddScoreValidate:
    @staticmethod
    def validate(tournament_id):
        ValidateCommandService.validate_tournament_exists(tournament_id)
        status = TournamentStatus.IN_PROGRESS
        ValidateCommandService.validate_tournament_status(tournament_id, status)
        ValidateCommandService.validate_round_matches(tournament_id, check_played=False)


class RoundAddScoreValidate:
    @staticmethod
    def validate(score1: float, score2: float):
        ValidateCommandService.validate_match_score(score1, score2)


class PlayerCreateValidate:
    @staticmethod
    def validate(national_chess_id: str, birthdate: date):
        ValidateCommandService.validate_national_chess_id(national_chess_id)
        ValidateCommandService.validate_date_format(birthdate)


class TournamentCreateValidate:
    @staticmethod
    def validate(start_date: date, end_date: date):
        ValidateCommandService.validate_date_format(start_date)
        ValidateCommandService.validate_date_format(end_date)


class TournamentAddPlayerValidate:
    @staticmethod
    def validate(tournament_id: int, players_ids: list):
        status = TournamentStatus.CREATED
        ValidateCommandService.validate_tournament_status(tournament_id, status)
        ValidateCommandService.validate_tournament_exists(tournament_id)
        for player_id in players_ids:
            ValidateCommandService.validate_player_exists(player_id)
        ValidateCommandService.validate_already_added_players(tournament_id, players_ids)


class ReportTournamentDetailsValidate:
    @staticmethod
    def validate(tournament_id):
        ValidateCommandService.validate_tournament_exists(tournament_id)


class TournamentStartValidate:
    @staticmethod
    def validate(tournament_id):
        status = TournamentStatus.CREATED
        ValidateCommandService.validate_tournament_status(tournament_id, status)
        ValidateCommandService.validate_minimum_players(tournament_id)


class TournamentEndValidate:
    @staticmethod
    def validate(tournament_id):
        status = TournamentStatus.IN_PROGRESS
        ValidateCommandService.validate_tournament_status(tournament_id, status)
        ValidateCommandService.validate_last_round_reached(tournament_id)
        ValidateCommandService.validate_round_matches(tournament_id, check_played=True)


class CreateRoundValidate:
    @staticmethod
    def validate(tournament_id):
        status = TournamentStatus.IN_PROGRESS
        ValidateCommandService.validate_tournament_status(tournament_id, status)
        ValidateCommandService.validate_round_matches(tournament_id, check_played=True)
