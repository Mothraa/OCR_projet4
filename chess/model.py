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
        # TODO appeler les setters
        # Génère un ID si aucun n'est spécifié
        self._id = kwargs.get('id', self.__create_id())
        self._name = kwargs.get("name", "")
        self._location = kwargs.get("location", "")
        self._status = kwargs.get("status", TournamentStatus.CREATED)
        self._start_date = kwargs.get("start_date", "")
        self._end_date = kwargs.get("end_date", "")
        self._description = kwargs.get("description", "")
        self._number_of_rounds = kwargs.get("number_of_rounds", 0)
        self._current_round_number = kwargs.get("current_round_number", 0)
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

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> TournamentStatus:
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

    @property
    def player_score_list(self):
        return self._player_score_list

    @player_score_list.setter
    def player_score_list(self, new_player_score_list):
        self._player_score_list = new_player_score_list

    @property
    def current_round_number(self):
        return self._current_round_number

    @current_round_number.setter
    def current_round_number(self, number):
        self._current_round_number = number

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

    @classproperty
    def tournaments_repertory(cls):
        return cls._tournaments_repertory

    def add_player_to_tournament(self, player):
        INIT_SCORE = 0.0
        # TODO : on enregistre que l'id du joueur plutot que l'instance pour régler un pb de serialisation json
        self.player_score_list.append((player.id, INIT_SCORE))

    def change_status(self, new_status: TournamentStatus):
        # TODO exceptions a reprendre
        actual_status = self.status
        if actual_status == TournamentStatus.TERMINATED:
            raise PermissionError("on ne peut modifier le statut d'un tournoi terminé")
        elif actual_status == TournamentStatus.IN_PROGRESS and new_status == TournamentStatus.CREATED:
            raise PermissionError("on ne peut repasser CREATED, un tournoi IN PROGRESS")
        else:
            self.status = new_status

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
    _matchs_list = None

    def __init__(self, **kwargs):
        # TODO appeler les setters
        self._id = kwargs.get("id")
        self._round_name = kwargs.get("round_name")
        self._start_date = kwargs.get("start_date")
        self._end_date = kwargs.get("end_date")
        self._matchs_list = kwargs.get("matchs_list", [])

    def add_matchs(self, matchs_list_to_add):
        """ format des matchs :
        ([player1, score_player1], [player2, score_player2])
        """
        self._matchs_list.extend(matchs_list_to_add)

    @property
    def id(self) -> int:
        return self._id

    @property
    def round_name(self) -> str:
        return self._round_name

    @property
    def matchs_list(self) -> list:
        return self._matchs_list

    @matchs_list.setter
    def matchs_list(self, new_matchs_list: list):
        self._matchs_list = new_matchs_list

    @property
    def start_date(self):
        """Get the start date of the round"""
        return self._start_date

    @start_date.setter
    def start_date(self, value=None):
        """Set the start date of the round"""
        self._start_date = value

    @property
    def end_date(self):
        """Get the end date of the round"""
        return self.end_date

    @end_date.setter
    def end_date(self, value=None):
        """Set the end date of the round"""
        self.end_date = value

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
    _tournaments_history = []
    _matchs_history = []
    _players_repertory = []

    def __init__(self, **kwargs):
        # TODO appeler les setters
        self._id = kwargs.get("id", self.__create_id())  # Generate ID if not specified
        self._national_chess_id = kwargs.get("national_chess_id")
        self._first_name = kwargs.get("first_name")
        self._last_name = kwargs.get("last_name")
        self._birthdate = kwargs.get("birthdate")
        self._tournaments_history = kwargs.get("tournaments_history", [])
        self._matchs_history = kwargs.get("matchs_history", [])
        # ajoute le joueur au répertoire de tous les joueurs
        Player._players_repertory.append(self)

    def __create_id(self) -> int:
        _id = len(Player._players_repertory)
        return _id

    @property
    def id(self):
        return self._id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @classproperty
    def players_repertory(cls):
        return cls._players_repertory

    # @property
    # def players_repertory(self) -> list:
    #     return self._players_repertory

    @property
    def tournaments_history(self) -> list:
        """History of played tournaments"""
        return self._tournaments_history

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

    def set_tournament_history(self, tournament: Tournament):
        """ Add a tournament in the player history"""
        if tournament.id in self.tournaments_history:
            # TODO exception a tester (test unitaire)
            raise TournamentAlreadyAddedError(tournament.__repr__)
        self._tournaments_history.append(tournament.id)

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
