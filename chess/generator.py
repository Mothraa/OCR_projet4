import random
import string
from datetime import datetime, timedelta


from faker import Faker
from . import model

class Creator:
    def __init__(self) -> None:
        self.fake = Faker(locale="fr_FR")

    def player(self, player_number: int):
        player_list = []
        for player in range(player_number):
            # appeler PlayerManagement plutot que le model
            player = model.Player(first_name=self.fake.unique.first_name(),
                                  last_name=self.fake.unique.last_name(),
                                  birthdate=self.fake.unique.date_of_birth(minimum_age=6, maximum_age=99),
                                  national_chess_id=self.fake.unique.bothify(text="??%%%%%").upper(),
                                  )
            player_list.append(player)
        return player_list

    def tournament(self, tournaments_number: int):

        DELTA_DATE = 3  # nombre de jours max entre début et fin d'un tournoi

        # on génère arbitrairement des dates de tournois sur une année
        list_date = []
        for _ in range(tournaments_number):
            list_date.append(self.fake.unique.date_this_year(before_today=False, after_today=True))
        list_date.sort()

        # génération des tournois avec attributs
        tournament_list = []

        for date_debut in list_date:
            location = self.fake.unique.city()
            date_fin = date_debut + timedelta(days=DELTA_DATE)
            # appeler TournamentManagement plutot que le model
            tournament = model.Tournament(name="Tournoi de {}".format(location),
                                          location=location,
                                          start_date=date_debut,
                                          end_date=self.fake.date_time_between(start_date=date_debut,
                                                                               end_date=date_fin
                                                                               ),
                                          number_of_rounds=random.randint(4, 8),
                                          description="Organisé par {}".format(self.fake.unique.name_nonbinary()),
                                          )
            tournament_list.append(tournament)

        return tournament_list

    def round(self):
        pass

    def match(self):
        pass

    @staticmethod
    def score(player1, player2):
        # scores randomisés et pondérés
        tirage = random.choices(['first', 'second', 'equal'], weights=(35, 35, 25))[0]
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