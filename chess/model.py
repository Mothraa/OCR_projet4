from enum import Enum  # , IntEnum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class TournamentStatus(ExtendedEnum):
    CREATED = 1
    IN_PROGRESS = 2
    TERMINATED = 3


class Player:
    id = None
    national_chess_id = None
    first_name = None
    last_name = None
    birthdate = None
    tournaments_history = []
    players_repertory = []

    def __init__(self, player_data):
        self.id = self.__create_id()
        self.national_chess_id = player_data.national_chess_id
        self.first_name = player_data.first_name
        self.last_name = player_data.last_name
        self.birthdate = player_data.birthdate
        Player.players_repertory.append(self)

    def __create_id(self):
        _id = len(Player.players_repertory)
        return _id

    @staticmethod
    def get_players_repertory():
        return Player.players_repertory

    @staticmethod
    def get_player_from_id(player_id: int):
        return Player.players_repertory[player_id]

    # def add_tournament_from(self, tournament: Tournament):
    #     self.tournaments_history.append(tournament)

    def add_tournament_from_id(self, tournament_id: int):
        self.tournaments_history.append(Tournament.get_tournament_from_id(tournament_id))

    def __repr__(self) -> str:
        return "ID {}: {} {}".format(self.id,
                                     self.first_name,
                                     self.last_name,
                                     )

    def encode(self):
        return self.__dict__


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
    player_list = []
    tournaments_repertory = []

    def __init__(self,  player_data):

        self.id = self.__create_id()
        self.name = player_data.name
        self.location = player_data.location
        self.status = TournamentStatus.CREATED
        self.start_date = player_data.start_date
        self.end_date = player_data.end_date
        self.description = player_data.description
        self.number_of_rounds = player_data.number_of_rounds

        Tournament.tournaments_repertory.append(self)

    def __create_id(self):
        _id = len(Tournament.tournaments_repertory)
        return _id

    # def default_rounds(self, number_of_rounds):
    #     if not number_of_rounds:
    #         rounds = self.DEFAULT_ROUND_NUMBER
    #     else:
    #         rounds = number_of_rounds
    #     return rounds

    def get_status(self) -> TournamentStatus:
        return self.status

    def change_status(self, new_status: TournamentStatus):
        if self.get_status() == TournamentStatus.TERMINATED:
            raise PermissionError("on ne peut modifier le statut d'un tournoi terminé")
        elif self.get_status() == TournamentStatus.IN_PROGRESS and new_status == TournamentStatus.CREATED:
            raise PermissionError("on ne peut repasser CREATED, un tournoi IN PROGRESS")
        else:
            self.status == new_status

    @staticmethod
    def get_tournaments_repertory():
        return Tournament.tournaments_repertory

    @staticmethod
    def get_tournament_from_id(tournament_id: int):
        return Tournament.tournaments_repertory[tournament_id]

    def __repr__(self) -> str:
        return "ID {} : {} - Du {} au {} - {} tours".format(self.id,
                                                            self.name,
                                                            self.start_date,
                                                            self.end_date,
                                                            self.number_of_rounds,
                                                            )


class Round:
    def __init__(self, **kwargs):
        self._id = kwargs.get("round_number")
        self.round_name = f"Round {kwargs.get("round_number")}"
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.matchs_list = []
