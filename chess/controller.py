import random
from operator import itemgetter

import logging
from chess.view import MainView, PlayerView, TournamentView, RoundView
from chess.model import Player, Tournament, Round, TournamentStatus
from chess.service import (
                        GeneratePlayerService,
                        GenerateTournamentService,
                        GenerateRoundService,
                        )


class MainController():
    view = None

    def __init__(self) -> None:
        # logging a passer en singleton pour pouvoir l'appeler partout ?
        logging.basicConfig(level=logging.DEBUG,
                            filename="chess.log",
                            filemode="a",  # "a",
                            encoding='utf-8',
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
            self.players_generate()
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

    def players_generate(self):
        command = self.view.player_generate_menu()
        self.generateur = GeneratePlayerService()

        for _ in range(command.choice):
            command_player = self.generateur.generate_player_all_attrs()
            self.player_create(command_player)
        #     player_list.append(player)
        # return player_list
        # self.generateur.add_players_all_attrs(command)
        # on retourne au menu
        self.player_menu()

    @staticmethod
    def add_tournament_history(player: Player, tournament: Tournament):
        player.tournaments_history.append(tournament)

    @staticmethod
    def add_match_history(player: Player, opponent: Player, result: enumerate):
        #TODO
        pass


class TournamentController():
    view = None
    tour = None

    def __init__(self) -> None:
        self.view = TournamentView()
        self.tour = RoundController()
        self.tournament_menu()

    def tournament_menu(self):
        self.view.tournament_menu()
        command = self.view.tournament_menu_user_choice()
        self.tournament_menu_select(command)

    def tournament_menu_select(self, command):
        if command.choice == 1:
            self.display_tournaments()
        elif command.choice == 2:
            self.display_tournament_details()
        elif command.choice == 3:
            self.tournament_menu_create()
        elif command.choice == 4:
            self.tournament_generate()
        elif command.choice == 5:
            self.tournament_add_players()
        elif command.choice == 6:
            self.tournament_menu_start()
        elif command.choice == 7:
            self.tournament_menu_continue()
        elif command.choice == 8:
            MainController()

    def display_tournaments(self):
        tournaments = Tournament.get_tournaments_repertory()
        self.view.display_tournaments(tournaments)
        # on retourne au menu
        self.tournament_menu()

    def display_tournament_details(self):
        command = self.view.tournament_details_get_tournament_id()
        tournament = Tournament.find_by_id(command.choice)
        # TODO 'nécessite de finir la serialisation de l'objet en text / json
        self.tournament_menu()

    def tournament_menu_create(self):
        command = self.view.tournament_create_menu()
        self.tournament_create(command)
        # on retourne au menu
        self.tournament_menu()

    def tournament_create(self, command):
        tournament = Tournament(command)
        logging.info("création d'un tournoi >> " + str(tournament))
        return tournament

    def tournament_generate(self):
        command = self.view.tournament_generate_menu()
        self.generateur = GenerateTournamentService()

        for _ in range(command.choice):
            command_tournament = self.generateur.generate_tournament_all_attrs()
            # trier par date de début avant création ?
            tournoi = self.tournament_create(command_tournament)
            print(f"Génération du tournoi >> {tournoi}")
        self.tournament_menu()

    def tournament_add_players(self):
        command_tournoi = self.view.tournament_add_players_get_tournament_id()
        command_players = self.view.tournament_add_players_get_players_id()
        self.add_players_by_ids(command_tournoi.choice, command_players.players_id_list)
        # TODO afficher le resultat
        # self.tournament_add_players_display()
        self.tournament_menu()

    def tournament_menu_start(self):
        command = self.view.tournament_menu_start()
        tournament = Tournament.find_by_id(command.choice)
        tournament.change_status(TournamentStatus.IN_PROGRESS)
        self.tour.generate_round()
        self.tournament_menu()

    def tournament_menu_continue(self):
        pass

    def add_players_by_ids(self, tournament_id: int, player_list: list[int]):
        for player_id in player_list:
            self.add_player(tournament_id, player_id)

    def add_player(self, tournament_id: int, player_id: int):
        # initialisation du score à 0
        INIT_VALUE = 0

        tournament = Tournament.find_by_id(tournament_id)
        player = Player.find_by_id(player_id)
        # on ajoute le joueur et son score a la liste du tournoi
        tournament.player_list.append([player, INIT_VALUE])
        # on ajoute également le tournoi à la liste de ceux joués par le joueur
        player.add_tournament_by_id(tournament.id)
        logging.info("Ajout du joueur [{}] au tournoi [{}]".format(player, tournament))
        # TODO afficher la liste des joueurs ajoutés en confirmation


class TournamentManagement():
    def __init__(self) -> None:
        pass
        #self.manage_round = RoundManagement()

    def create(self, **kwargs) -> Tournament:
        tournament = Tournament(**kwargs)
        self.__create_round(tournament, tournament.number_of_rounds)
        return tournament

    def __create_round(self, tournament: Tournament, nb_of_rounds: int):
        for round_number in range(1, nb_of_rounds + 1):
            round = self.manage_round.create(round_number=round_number)
            self.__add_round(tournament, round)

    def __add_round(self, tournament: Tournament, round: Round):
        tournament.rounds_list.append(round)


class RoundController():
    view = None
    service = None

    def __init__(self):
        self.view = RoundView()
        self.service = GenerateRoundService()
    # def generate_round(self, command):
    #  tournament = Tournament.find_by_id(command.getTournamentCode())
    #  players = Player.find_by_tournaments(tournament)
    #  games = GenerateRoundUseCase().generate(tournament, players)
    #  Round.create(tournament, games)
    #  print("Le tournoi a bien été ajouté")

    def generate_round(self, command):
        # quel tour est en cours, et si tous les scores ont bien été renseignés
        # demande confirmation de fin de round
        command = self.view.generate_round_menu()
        # ajouter date et heure de fin de l'ancien round
        # ajouter date et heure de début du nouveau round

        #games = GenerateRoundUseCase().generate(tournament, players)
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
