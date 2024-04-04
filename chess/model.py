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
        _id = len(Player.players_repertory) + 1
        return _id

    @staticmethod
    def get_players_repertory():
        return Player.players_repertory

    def __repr__(self) -> str:
        return "id={}: {} {}".format(self.id, self.first_name, self.last_name)

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
    tournament_repertory = []

    def __init__(self,  player_data):

        self.id = self.__create_id()
        self.name = player_data.name
        self.location = player_data.location
        self.status = TournamentStatus.CREATED
        self.start_date = player_data.start_date
        self.end_date = player_data.end_date
        self.description = player_data.description
        self.number_of_rounds = player_data.number_of_rounds

        Tournament.tournament_repertory.append(self)

    def __create_id(self):
        _id = len(Tournament.tournament_repertory) + 1
        return _id

    # def default_rounds(self, number_of_rounds):
    #     if not number_of_rounds:
    #         rounds = self.DEFAULT_ROUND_NUMBER
    #     else:
    #         rounds = number_of_rounds
    #     return rounds

    @staticmethod
    def get_tournament_repertory():
        return Tournament.tournament_repertory  # print(Player.player_repertory)

    def __repr__(self) -> str:
        return "{} : {} - date : {}".format(self.id, self.name, self.start_date)


class Round:
    def __init__(self, **kwargs):
        self._id = kwargs.get("round_number")
        self.round_name = f"Round {kwargs.get("round_number")}"
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.matchs_list = []
