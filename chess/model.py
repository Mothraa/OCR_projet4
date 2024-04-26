from operator import itemgetter
from datetime import datetime

from chess.utils import TournamentStatus


class Tournament:
    id = None
    name = None
    location = None
    status = None
    start_date = None
    end_date = None
    description = None
    number_of_rounds = None
    current_round_number = None
    rounds_list = []
    player_score_list = []
    tournaments_repertory = []

    def __init__(self, **kwargs):
        # Génère un ID si aucun n'est spécifié
        self.id = kwargs.get('id', self.__create_id())
        self.name = kwargs.get("name", "")
        self.location = kwargs.get("location", "")
        self.status = kwargs.get("status", TournamentStatus.CREATED)
        self.start_date = kwargs.get("start_date", "")
        self.end_date = kwargs.get("end_date", "")
        self.description = kwargs.get("description", "")
        self.number_of_rounds = kwargs.get("number_of_rounds", 0)
        self.current_round_number = kwargs.get("current_round_number", 0)
        self.rounds_list = kwargs.get("rounds_list", [])
        self.player_score_list = kwargs.get("player_score_list", [])

        Tournament.tournaments_repertory.append(self)

    def __create_id(self) -> int:
        _id = len(Tournament.tournaments_repertory)
        return _id

    def get_status(self) -> TournamentStatus:
        return self.status

    def get_player_score_list(self):
        return self.player_score_list

    def set_player_score_list(self, new_player_score_list):
        self.player_score_list = new_player_score_list

    def get_current_round_number(self):
        return self.current_round_number

    def get_current_round(self):
        round_indice = self.get_current_round_number() - 1
        chess_round = self.rounds_list[round_indice]
        return chess_round

    def get_number_of_rounds(self):
        return self.number_of_rounds

    def add_player_to_tournament(self, player):
        INIT_SCORE = 0.0
        # TODO : on enregistre que l'id du joueur plutot que l'instance pour régler un pb de serialisation json
        self.player_score_list.append((player.id, INIT_SCORE))

    def change_status(self, new_status: TournamentStatus):
        actual_status = self.get_status()
        if actual_status == TournamentStatus.TERMINATED:
            raise PermissionError("on ne peut modifier le statut d'un tournoi terminé")
        elif actual_status == TournamentStatus.IN_PROGRESS and new_status == TournamentStatus.CREATED:
            raise PermissionError("on ne peut repasser CREATED, un tournoi IN PROGRESS")
        else:
            self.status = new_status

    def sort_players_by_score(self):
        # la liste des joueurs est de la forme (Player, score)
        self.player_score_list.sort(key=itemgetter(1), reverse=True)

    @staticmethod
    def get_tournaments_repertory():
        return Tournament.tournaments_repertory

    @staticmethod
    def find_by_id(tournament_id: int):
        return Tournament.tournaments_repertory[tournament_id]

    def __repr__(self) -> str:
        return "ID {} : {} - {} tours".format(self.id,
                                              self.name,
                                              self.number_of_rounds,
                                              )


class ChessRound:
    id = None
    round_name = None
    start_date = None
    end_date = None
    matchs_list = []

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.round_name = kwargs.get("round_name")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.matchs_list = kwargs.get("matchs_list", [])

    def add_matchs(self, matchs_list_to_add):
        """ format des matchs :
        ([player1, score_player1], [player2, score_player2])
        """
        self.matchs_list.append(matchs_list_to_add)

    def get_round_name(self) -> str:
        return self.round_name

    def get_matchs_list(self) -> list:
        return self.matchs_list

    def set_start_date(self, date=None):
        """Set the start_date of the round. If not specified, take the current date """
        if date is None:
            date = datetime.now()
        self.start_date = date

    def set_end_date(self, date=None):
        """Set the end_date of the round. If not specified, take the current date """
        if date is None:
            date = datetime.now()
        self.end_date = date


class Player:
    id = None
    national_chess_id = None
    first_name = None
    last_name = None
    birthdate = None
    tournaments_history = []
    matchs_history = []
    players_repertory = []

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", self.__create_id())  # Generate ID if not specified
        self.national_chess_id = kwargs.get("national_chess_id")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.birthdate = kwargs.get("birthdate")
        self.tournaments_history = kwargs.get("tournaments_history", [])
        self.matchs_history = kwargs.get("matchs_history", [])
        Player.players_repertory.append(self)

    def __create_id(self) -> int:
        id = len(Player.players_repertory)
        return id

    @staticmethod
    def get_players_repertory() -> list:
        """List of all players"""
        return Player.players_repertory

    @staticmethod
    def find_by_id(player_id: int):
        """Return a player from his ID"""
        return Player.players_repertory[player_id]

    def set_tournament_history(self, tournament: Tournament):
        """ Add a tournament in the player history"""
        if tournament.id not in self.tournaments_history:
            self.tournaments_history.append(tournament.id)
        else:
            print("Le tournoi {} a déjà été ajouté à l'historique.".format(tournament.name))

    def get_tournament_history(self) -> list:
        """History of played tournaments"""
        return self.tournaments_history

    def set_match_history(self, **kwargs):
        """Add match in the player history"""
        tournament_id = kwargs.get("tournament_id")
        round_id = kwargs.get("round_id")
        opponent_id = kwargs.get("opponent_id")
        score_player = kwargs.get("score_player")
        score_opponent = kwargs.get("score_opponent")
        self.matchs_history.append((tournament_id,
                                    round_id,
                                    opponent_id,
                                    score_player,
                                    score_opponent))

    def get_matchs_history(self) -> list:
        """ History of all matchs played :
            format : list of tuples => (tournament ID, round ID, opponent ID, player_score, opponent_score)
        """
        return self.matchs_history

    def get_matchs_history_by_tournament(self, tournament: Tournament) -> list:
        """ History of matchs by tournament :
            format : list of tuples => (tournament ID, round ID, opponent ID, player_score, opponent_score)
        """
        full_list = self.get_matchs_history()
        list_history = [x for x in full_list if x[0] == tournament.id]
        return list_history

    def __repr__(self) -> str:
        return "ID {}: {} {}".format(self.id,
                                     self.first_name,
                                     self.last_name,
                                     )
