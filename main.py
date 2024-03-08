
import random
import string
import logging

from faker import Faker

from datetime import datetime
from zoneinfo import ZoneInfo


class Player:

    uid = ""
    national_chess_uid = ""
    first_name = ""
    surname = ""
    birthdate = ""
    tournaments_history = []
    player_repertory = []

    def __init__(self, **kwargs):
        # for key, value in kwargs.items():
        #     setattr(self, key, value)

        self.uid = self.__create_uid()
        self.first_name = kwargs.get("first_name")
        self.surname = kwargs.get("surname")
        self.birthdate = kwargs.get("birthdate")
        self.national_chess_uid = kwargs.get("national_chess_uid")

        Player.player_repertory.append(self)

    def __create_uid(self):
        uid = len(Player.player_repertory) + 1
        return uid

    @staticmethod
    def show_player_repertory():
        return print(Player.player_repertory)

    def __repr__(self) -> str:
        return "uid={}: {} {}".format(self.uid, self.first_name, self.surname)

class Tournament:
    pass

class Round:
    pass

class Match:
    pass


class Creator:
    def __init__(self) -> None:
        self.fake = Faker(locale="fr_FR")


    def player(self, player_number: int):
        playerlist = []
        for i in range(player_number):
            toto = Player(first_name=self.fake.unique.first_name(),
                          surname=self.fake.unique.last_name(),
                          birthdate=self.fake.unique.date_of_birth(minimum_age=6, maximum_age=99),
                          national_chess_uid=self.fake.unique.bothify(text="??%%%%%").upper(),
                          )
            playerlist.append(toto)
            i += 1
        return playerlist


    def tournament(self):
        #date_between_dates / date_time_between / future_datetime

        print(self.fake.unique.address()) #city()
        pass
    
    def round(self):
        pass

    def match(self):
        pass



if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        filename="logfile.log",
                        filemode="w",#"a"
                        format='%(asctime)s - %(levelname)s : %(message)s')#WARNING

    timezone = ZoneInfo("Europe/Paris")

    creator = Creator()
    liste = creator.player(3)
    Player.show_player_repertory()

#    logging.warning("whoaa!")

    jour = datetime.now(tz=timezone)
