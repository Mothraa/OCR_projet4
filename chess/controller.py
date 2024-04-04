import random
from datetime import date
from operator import itemgetter
import logging
from chess.view import MainView, PlayerView, TournamentView
from chess.model import Player, Tournament, Round
from chess.service import (
                        GeneratePlayerService,
                        # GenerateTournamentService,
                        # GenerateRoundService,
                        )


class MainController():
    view = None

    def __init__(self) -> None:
        # logging a passer en singleton pour pouvoir l'appeler partout ?
        logging.basicConfig(level=logging.DEBUG,
                            filename="chess.log",
                            filemode="a",  # "a"
                            format='%(asctime)s - %(levelname)s : %(message)s')  # WARNING
        # pour eviter que faker nous spam de logs
        logging.getLogger('faker').setLevel(logging.ERROR)

        self.view = MainView()
        command = self.view.get_user_choice()
        self.main_menu_select(command)

        # logging.warning("whoaa!")

        # self.manage_player = PlayerManagement()
        # self.manage_tournament = TournamentManagement()

    def main_menu_select(self, command):
        if command.choice == 1:  # MainOption.PLAYER_MENU_OPTION:
            #controller = PlayerController()
            PlayerController()
        elif command.choice == 2:  # MainOption.TOURNAMENT_MENU_OPTION:
            TournamentController()
        elif command.choice == 3:  # MainOption.CLOSE_PROGRAM_OPTION:
            # ajouter message de départ
            pass


class PlayerController():
    view = None
    generateur = None

    def __init__(self) -> None:
        self.view = PlayerView()
        self.player_menu()

    def player_menu(self):
        self.view.player_menu()
        command = self.view.get_user_choice()
        self.player_menu_select(command)

    def player_menu_select(self, command):
        if command.choice == 1:
            self.display_players()
        elif command.choice == 2:
            self.player_create_menu()
        elif command.choice == 3:
            self.players_generate_menu()
        elif command.choice == 4:
            MainController()

    def display_players(self):
        # TODO Player a instancier ?
        players = Player.get_players_repertory()
        self.view.display_players(players)
        # on retourne au menu
        self.player_menu()

    def player_create_menu(self):
        command = self.view.player_create_menu()
        self.player_create(command)
        # on retourne au menu
        self.player_menu()

    def player_create(self, command):
        player = Player(command)
        logging.info("création du joueur >> " + str(player))
        return player

    def players_generate_menu(self):
        command = self.view.player_generate_menu()
        self.generateur = GeneratePlayerService()
        player_list = []

        for player in range(command.choice):
            command_player = self.generateur.generate_player_all_attrs()
            player = self.player_create(command_player)
        #     player_list.append(player)
        # return player_list
        # self.generateur.add_players_all_attrs(command)
        # on retourne au menu
        self.player_menu()

    @staticmethod
    def get_player_by_id(player_id: int) -> Player:
        return Player.player_repertory[player_id]

    @staticmethod
    def add_tournament_history(player: Player, tournament: Tournament):
        player.tournaments_history.append(tournament)

    @staticmethod
    def add_match_history(player: Player, opponent: Player, result: enumerate):
        pass


class TournamentController():
    view = None

    def __init__(self) -> None:
        self.view = TournamentView()
        self.tournament_menu()

    def tournament_menu(self):
        self.view.tournament_menu()
        command = self.view.get_user_choice()
        self.tournament_menu_select(command)

    def tournament_menu_select(self, command):
        if command.choice == 1:
            self.display_tournaments()
        elif command.choice == 2:
            self.tournament_menu_create()
        elif command.choice == 3:
            self.tournament_menu_generate()
        elif command.choice == 4:
            self.tournament_menu_start()
        elif command.choice == 5:
            self.tournament_menu_continue()
        elif command.choice == 6:
            MainController()

    def display_tournaments(self):
        pass

    def tournament_menu_create(self):
        command = self.view.tournament_create_menu()
        self.tournament_create(command)
        # on retourne au menu
        self.tournament_menu()

    def tournament_create(self, command):
        tournament = Tournament(command)
        logging.info("création d'un tournoi >> " + str(tournament))
        return tournament


class TournamentManagement():
    def __init__(self) -> None:
        self.manage_round = RoundManagement()

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

class RoundController():
    view = None

    def __init__(self):
      pass
  #  self.view = view
  
  # def generate_round(self, command):
  #  tournament = Tournament.find_by_code(command.getTournamentCode())
  #  players = Player.find_by_tournaments(tournament)
  #  games = GenerateRoundUseCase().generate(tournament, players)
  #  Round.create(tournament, games)
  #  print("Le tournoi a bien été ajouté")

    def generate_round(self, command):
    # command = self.view.generate_round_menu()
    # games = GenerateRoundUseCase().generate(tournament, players)
        print("Le tour a bien été ajouté")


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

class MatchController():
    def __init__(self) -> None:
        pass

    def create():
        pass

    def check_number_of_players():
        # a ne faire que sur le round ?
        pass
