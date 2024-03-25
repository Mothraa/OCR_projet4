
class Tournament:

    DEFAULT_ROUND_NUMBER = 4
    tournament_repertory = []

    def __init__(self,  **kwargs):

        self.id = self.__create_id()
        self.name = kwargs.get("name")
        self.location = None
        self.status = None
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.description = None
        self.number_of_rounds = self.default_rounds(kwargs.get("number_of_rounds"))
        self.current_round_number = None
        self.rounds_list = []
        self.player_list = []

        Tournament.tournament_repertory.append(self)

    def __create_id(self):
        _id = len(Tournament.tournament_repertory) + 1
        return _id

    def default_rounds(self, number_of_rounds):
        if not number_of_rounds:
            rounds = self.DEFAULT_ROUND_NUMBER
        else:
            rounds = int(number_of_rounds)
        return rounds

    def __repr__(self) -> str:
        return "{} : {} / dates : {} to {}".format(self.id, self.name, self.start_date, self.end_date)


class Round:
    def __init__(self, **kwargs):
        self._id = kwargs.get("round_number")
        self.round_name = f"Round {kwargs.get("round_number")}"
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.matchs_list = []


class Player:

    player_repertory = []

    def __init__(self, **kwargs):
        # for key, value in kwargs.items():
        #     setattr(self, key, value)

        self.id = self.__create_id()
        self.national_chess_id = kwargs.get("national_chess_id")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.birthdate = kwargs.get("birthdate")
        self.tournaments_history = []
        Player.player_repertory.append(self)

    def __create_id(self):
        _id = len(Player.player_repertory) + 1
        return _id

    @staticmethod
    def get_player_repertory():
        return Player.player_repertory  # print(Player.player_repertory)

    def __repr__(self) -> str:
        return "id={}: {} {}".format(self.id, self.first_name, self.last_name)

    def encode(self):
        return self.__dict__
