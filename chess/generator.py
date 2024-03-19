import random
import string

from faker import Faker
from . import model

class Creator:
    def __init__(self) -> None:
        self.fake = Faker(locale="fr_FR")

    def player(self, player_number: int):
        playerlist = []
        for i in range(player_number):
            player = model.Player(first_name=self.fake.unique.first_name(),
                                  last_name=self.fake.unique.last_name(),
                                  birthdate=self.fake.unique.date_of_birth(minimum_age=6, maximum_age=99),
                                  national_chess_id=self.fake.unique.bothify(text="??%%%%%").upper(),
                                  )
            playerlist.append(player)
            i += 1
        return playerlist

    def tournament(self):
        #date_between_dates / date_time_between / future_datetime

        print(self.fake.unique.address())  # city()
        pass

    def round(self):
        pass

    def match(self):
        pass

    @staticmethod
    def score(player1, player2):
        tirage = random.choice(['first', 'second', 'equal'])
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


# #     print(toto)
# #     print(type(toto))
# #     save = SaveAsJSON()
# #     save.player(toto)