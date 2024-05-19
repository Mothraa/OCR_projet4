from operator import itemgetter

from chess.utils import TournamentStatus
from chess.exceptions import TournamentAlreadyAddedError


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class Tournament:
    _id = None
    _name = None
    _location = None
    _status = None
    _start_date = None
    _end_date = None
    _description = None
    _number_of_rounds = None
    _current_round_number = None
    _rounds_list = []
    _player_score_list = []
    _tournaments_repertory = []

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get("name")
        self.location = kwargs.get("location")
        self.status = kwargs.get("status", TournamentStatus.CREATED)
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.description = kwargs.get("description")
        self.number_of_rounds = kwargs.get("number_of_rounds", 4)
        self.current_round_number = kwargs.get("current_round_number", 0)
        self._rounds_list = kwargs.get("rounds_list", [])
        self._player_score_list = kwargs.get("player_score_list", [])
        # ajoute le tournoi au répertoire de tous les tournois
        Tournament._tournaments_repertory.append(self)

    def __create_id(self) -> int:
        _id = len(Tournament._tournaments_repertory)
        return _id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id):
        # Génère un ID si aucun n'est spécifié
        if not new_id:
            self._id = self.__create_id()
        else:
            self._id = new_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, new_location):
        self._location = new_location

    @property
    def status(self) -> TournamentStatus:
        return self._status

    @status.setter
    def status(self, new_status: TournamentStatus):
        self.change_status(new_status)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, new_start_date):
        self._start_date = new_start_date

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, new_end_date):
        self._end_date = new_end_date

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @property
    def player_score_list(self):
        return self._player_score_list

    @player_score_list.setter
    def player_score_list(self, new_player_score_list):
        self._player_score_list = new_player_score_list

    def current_round(self):
        round_indice = self.current_round_number - 1
        chess_round = self._rounds_list[round_indice]
        return chess_round

    @property
    def rounds_list(self) -> list:
        return self._rounds_list

    @property
    def number_of_rounds(self):
        return self._number_of_rounds

    @number_of_rounds.setter
    def number_of_rounds(self, new_number_of_rounds):
        self._number_of_rounds = new_number_of_rounds

    @property
    def current_round_number(self):
        return self._current_round_number

    @current_round_number.setter
    def current_round_number(self, new_current_round_number):
        self._current_round_number = new_current_round_number

    @classproperty
    def tournaments_repertory(cls):
        return cls._tournaments_repertory

    def add_player_to_tournament(self, player):
        INIT_SCORE = 0.0
        self.player_score_list.append((player.id, INIT_SCORE))

    def change_status(self, new_status: TournamentStatus):
        if not new_status:
            raise ValueError("indiquer une nouvelle valeur de statut")
        actual_status = self.status
        if actual_status == TournamentStatus.TERMINATED:
            raise PermissionError("on ne peut modifier le statut d'un tournoi terminé")
        elif actual_status == TournamentStatus.IN_PROGRESS and new_status == TournamentStatus.CREATED:
            raise PermissionError("on ne peut repasser CREATED, un tournoi IN PROGRESS")
        else:
            self._status = new_status

    def sort_players_by_score(self):
        """Sort the list of players by score in descending order"""
        # la liste des joueurs est de la forme (Player, score)
        self.player_score_list.sort(key=itemgetter(1), reverse=True)

    @staticmethod
    def find_by_id(tournament_id: int):
        if not isinstance(tournament_id, int):
            raise ValueError("L'ID du tournoi doit être un entier")
        for tournament in Tournament.tournaments_repertory:
            if tournament.id == tournament_id:
                return tournament
        raise ValueError("Aucun tournoi trouvé avec cet ID")

    def to_json(self):
        return {
                "id": self._id,
                "name": self._name,
                "location": self._location,
                "status": self._status,
                "start_date": self._start_date,
                "end_date": self._end_date,
                "description": self._description,
                "number_of_rounds": self._number_of_rounds,
                "current_round_number": self._current_round_number,
                "rounds_list": self._rounds_list,
                "player_score_list": self._player_score_list,
                }

    def __repr__(self) -> str:
        return "ID {} : {} - {} tours".format(self.id,
                                              self.name,
                                              self.number_of_rounds,
                                              )


class ChessRound:
    _id = None
    _round_name = None
    _start_date = None
    _end_date = None
    _matchs_list = []

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.round_name = kwargs.get("round_name")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.matchs_list = kwargs.get("matchs_list") if kwargs.get("matchs_list") is not None else []

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def round_name(self) -> str:
        return self._round_name

    @round_name.setter
    def round_name(self, new_round_name):
        self._round_name = new_round_name

    @property
    def start_date(self) -> str:
        """Get the start date of the round"""
        return self._start_date

    @start_date.setter
    def start_date(self, value=None):
        """Set the start date of the round"""
        self._start_date = value

    @property
    def end_date(self):
        """Get the end date of the round"""
        return self._end_date

    @end_date.setter
    def end_date(self, value=None):
        """Set the end date of the round"""
        self._end_date = value

    @property
    def matchs_list(self) -> list:
        return self._matchs_list

    @matchs_list.setter
    def matchs_list(self, new_matchs_list: list):
        """add matchs to existing matches list"""
        if not isinstance(new_matchs_list, list):
            raise ValueError("new_matchs_list doit être une liste")
        self._matchs_list.extend(new_matchs_list)

    def to_json(self):
        return {
                "id": self._id,
                "round_name": self._round_name,
                "start_date": self._start_date,
                "end_date": self._end_date,
                "matchs_list": self._matchs_list,
                }


class Player:
    _id = None
    _national_chess_id = None
    _first_name = None
    _last_name = None
    _birthdate = None
    _matchs_history = []
    _players_repertory = []

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.national_chess_id = kwargs.get("national_chess_id")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.birthdate = kwargs.get("birthdate")
        self._tournaments_history = []
        self.tournaments_history = kwargs.get("tournaments_history", [])
        self.matchs_history = kwargs.get("matchs_history", [])
        # ajoute le joueur au répertoire de tous les joueurs
        Player._players_repertory.append(self)

    def __create_id(self) -> int:
        _id = len(Player._players_repertory)
        return _id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id):
        # Generate an ID if not specified
        if not new_id:
            self._id = self.__create_id()
        else:
            self._id = new_id

    @property
    def national_chess_id(self):
        return self._national_chess_id

    @national_chess_id.setter
    def national_chess_id(self, new_national_chess_id):
        self._national_chess_id = new_national_chess_id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_first_name):
        self._first_name = new_first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self._last_name = new_last_name

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, new_birthdate):
        self._birthdate = new_birthdate

    @classproperty
    def players_repertory(cls):
        return cls._players_repertory

    @property
    def tournaments_history(self) -> list:
        """History of played tournaments"""
        return self._tournaments_history

    @tournaments_history.setter
    def tournaments_history(self, tournaments_ids):
        """Add a tournament ID or a list of tournaments IDs to the history of one player"""
        if tournaments_ids in self.tournaments_history:
            raise TournamentAlreadyAddedError(tournaments_ids)
        elif isinstance(tournaments_ids, int):
            # Si un seul identifiant
            self._tournaments_history.append(tournaments_ids)
        elif isinstance(tournaments_ids, list):
            # Si une liste d'identifiants
            self._tournaments_history.extend(tournaments_ids)
        else:
            raise ValueError("tournaments_ids doit être un entier ou une liste d'entiers")

    @property
    def matchs_history(self) -> list:
        """ History of all matchs played :
            format : list of tuples => (tournament ID, round ID, opponent ID, player_score, opponent_score)
        """
        return self._matchs_history

    @matchs_history.setter
    def matchs_history(self, value):
        self._matchs_history = value

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

    def matchs_history_by_tournament(self, tournament: Tournament) -> list:
        """ History of matchs by tournament :
            format : list of tuples => (tournament ID, round ID, opponent ID, player_score, opponent_score)
        """
        full_list = self.matchs_history
        list_history = [x for x in full_list if x[0] == tournament.id]
        return list_history

    @staticmethod
    def get_players_repertory() -> list:
        """List of all players"""
        return Player.players_repertory

    @staticmethod
    def find_by_id(player_id: int):
        """Return a player from his ID"""
        if not isinstance(player_id, int):
            raise ValueError("L'ID du player doit être un entier")
        for player in Player.players_repertory:
            if player.id == player_id:
                return player
        raise ValueError("Aucun joueur trouvé avec cet ID")

    def to_json(self):
        return {
            "id": self._id,
            "national_chess_id": self._national_chess_id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "birthdate": self._birthdate,
            "tournaments_history": self._tournaments_history,
            "matches_history": self._matchs_history
        }

    def __repr__(self) -> str:
        return "ID {}: {} {}".format(self.id,
                                     self.first_name,
                                     self.last_name,
                                     )
