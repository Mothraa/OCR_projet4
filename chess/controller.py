import random
from datetime import date
from operator import itemgetter
import logging

from chess.model import Player, Tournament, Round
from chess.generator import Creator


class Controller():
    def __init__(self) -> None:
        # logging a passer en singleton pour pouvoir l'appeler partout ?
        logging.basicConfig(level=logging.DEBUG,
                            filename="chess.log",
                            filemode="a",  # "a"
                            format='%(asctime)s - %(levelname)s : %(message)s')  # WARNING
        # pour eviter que faker nous spam de logs
        logging.getLogger('faker').setLevel(logging.ERROR)

# # #    logging.warning("whoaa!")
        self.manage_player = PlayerManagement()
        self.manage_tournament = TournamentManagement()

    def run(self):
        pass
        # afficher le menu principal

        # tournoi1 = self.manage_tournament.create(name="Tournoi en arène",
        #                                          start_date="2054-01-01",
        #                                          end_date="2054-05-01",
        #                                          number_of_rounds="6",
        #                                          )

        # tournoi2 = self.manage_tournament.create(
        #                                         name="Tournoi sur pilotis",
        #                                         start_date="2054-04-02",
        #                                         end_date="2054-08-02",
        #                                         )

        # player1 = self.manage_player.create(first_name="Jon",
        #                                     last_name="Jon",
        #                                     birthdate="1990-01-01",
        #                                     national_chess_id="JJ123",
        #                                     )

        # player2 = self.manage_player.create(first_name="Michel",
        #                                     last_name="Michel",
        #                                     birthdate="1988-05-15",
        #                                     national_chess_id="MM456",
        #                                     )

        # # génération aléatoire de joueurs TODO : passer Creator en tant que décorateur

        # player_list = self.createur.player(10)

        # # on ajoute les joueurs au tournoi
        # for player in player_list:
        #     self.manage_tournament.add_player(tournoi1, player)

        # # on génère l'ensemble des matchs
        # self.manage_tournament.manage_round.create_matchs(tournoi1)


class InputManagement():
    def __init__():
        pass

    # TODO : passer les verifs sur la classe InputManagement ou design pattern command ?
    @staticmethod
    def check_input(input_str: str, *args: type):
        check = False
        try:
            for input_type in args:
                if input_type == str and isinstance(input_str, str):
                    check = True
                elif input_type == int and isinstance(int(input_str), int):
                    check = True
                elif input_type == date and date.fromisoformat(input_str):
                    check = True
                # TODO : ajouter le cas None
                # TODO : si plusieurs cas, le None l'emporte
                # elif (input_type is None) and (input_str == ""):
                # elif (input_type is type(None)) and (input_str == ""):
                #     check = True
            # except ValueError:
            #     print("Format incorrect")
        except Exception as e:
            print(e)
        
        return check

    @staticmethod
    def check_dates(self, start_date, end_date):
        """vérification :
            - du format date
            - que la date de début est avant la date de fin
            - que les dates sont à venir
        """
        pass

    @staticmethod
    def check_chess_id(self):
        pass


class PlayerManagement():
    def __init__(self) -> None:
        pass

    def create(self, **kwargs):
        player = Player(**kwargs)
        logging.info("création du joueur >> " + str(player))
        return player

    @staticmethod
    def get_player_by_id(player_id: int) -> Player:
        return Player.player_repertory[player_id]

    @staticmethod
    def add_tournament(player: Player, tournament: Tournament):
        player.tournaments_history.append(tournament)

    @staticmethod
    def add_match(player: Player, opponent: Player, result: enumerate):
        pass


class TournamentManagement():
    def __init__(self) -> None:
        self.manage_round = RoundManagement()
        pass

    def create(self, **kwargs) -> Tournament:
        tournament = Tournament(**kwargs)
        self.__create_round(tournament, tournament.number_of_rounds)
        return tournament

    @staticmethod
    def get_tournament_by_id(tournament_id: int) -> Tournament:
        return Tournament.tournament_repertory[tournament_id]

    def add_players_from_ids(self, tournament_id: int, player_list: list):
        tournament = self.get_tournament_by_id(tournament_id)
        for player_id in player_list:
            player = PlayerManagement.get_player_by_id(player_id)
            self.add_player(tournament, player)

    def add_player(self, tournament: Tournament, player: Player):
        # initialisation du score à 0
        score = 0
        # on ajoute le joueur et son score a la liste du tournoi
        # TODO a passer en dict
        tournament.player_list.append([player, score])
        # on ajoute également le tournoi à la liste de ceux joués par le joueur
        PlayerManagement.add_tournament(player, tournament)

    def __create_round(self, tournament: Tournament, nb_of_rounds: int):
        for round_number in range(1, nb_of_rounds + 1):
            round = self.manage_round.create(round_number=round_number)
            self.__add_round(tournament, round)

    def __add_round(self, tournament: Tournament, round: Round):
        tournament.rounds_list.append(round)


class RoundManagement():
    def __init__(self) -> None:
        pass

    def create(self, **kwargs):
        round = Round(**kwargs)
        return round

    def create_matchs(self, tournament: Tournament):
        for round_number in range(tournament.number_of_rounds):
            # on génère des couples de joueurs et un score aléatoire
            self.create_players_peers(tournament, round_number)
            # on tri la liste des joueurs suivant les résultats
            tournament.player_list.sort(key=itemgetter(1), reverse=True)
        pass

    def create_players_peers(self, tournament: Tournament, round_number: int) -> None:

        actual_round_list = tournament.player_list.copy()

        while len(actual_round_list) >= 2:

            # au premier tour random sur les paires
            if round_number == 0:  # le premier round est celui d'indice 0
                player1 = actual_round_list.pop(random.randrange(len(actual_round_list)))
                player2 = actual_round_list.pop(random.randrange(len(actual_round_list)))
            else:
                # ensuite on prend suivant l'ordre du classement
                player1 = actual_round_list.pop(0)
                # On évite de créer des matchs identiques
                i = 0
                while len(actual_round_list) > 1:
                    # on regarde si le match a déjà été jouer, si oui on passe au suivant
                    if player2 in player1.tournaments_history[tournament.id][i]:
                        i += 1
                    else:
                        player2 = actual_round_list.pop(0)
                        break
                # si il ne reste plus qu'un joueur sur la liste
                if len(actual_round_list) == 1:
                    player2 = actual_round_list.pop(0)


            # TODO : a déplacer dans fonction dédiée
            # génération d'un score aléatoire
            result_match = self.match_add_scores(player1, player2)
            tournament.rounds_list[round_number].matchs_list.append(result_match)

            # mise à jour des scores généraux du tournoi
            tournament.player_list[tournament.player_list.index(player1)][1] += result_match[0][1]
            tournament.player_list[tournament.player_list.index(player2)][1] += result_match[1][1]

    def match_add_scores(self, player1: Player, player2: Player) -> tuple:
        return Creator.score(player1, player2)

    def check_number_of_players():
        pass


class MatchManagement():
    def __init__(self) -> None:
        pass

    def create():
        pass

    def check_number_of_players():
        # a ne faire que sur le round ?
        pass
