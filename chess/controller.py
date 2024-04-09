import random
from datetime import datetime

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
    service = None

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
        self.service = GeneratePlayerService()

        for _ in range(command.choice):
            command_player = self.service.generate_player_all_attrs()
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
    service = None

    def __init__(self) -> None:
        self.view = TournamentView()
        self.tour = RoundController()
        self.service = GenerateTournamentService()
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
            self.tournament_menu_add_scores()
        elif command.choice == 8:
            self.tournament_menu_continue()
        elif command.choice == 9:
            self.tournament_menu_end()
        elif command.choice == 10:
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

        for _ in range(command.choice):
            command_tournament = self.service.generate_tournament_all_attrs()
            # trier par date de début avant création ?
            tournoi = self.tournament_create(command_tournament)
            print(f"Génération du tournoi >> {tournoi}")
        self.tournament_menu()

    def tournament_add_players(self):
        command = self.view.tournament_add_players()
        self.add_players_by_ids(command.tournament_id, command.players_id_list)
        # TODO afficher le resultat
        # self.tournament_add_players_display()
        self.tournament_menu()

    def tournament_menu_start(self):
        command = self.view.tournament_menu_start()
        tournament = Tournament.find_by_id(command.choice)
        self.tournament_init(tournament)
        self.tour.create_first_round(tournament)
        self.tournament_menu()

    def tournament_menu_add_scores(self):
        self.tour.add_scores()
        self.tournament_menu()

    def tournament_init(self, tournament: Tournament):
        tournament.current_round_number = 0
        tournament.change_status(TournamentStatus.IN_PROGRESS)

    def tournament_menu_continue(self):
        self.tour.create_next_round()
        self.tournament_menu()

    def tournament_menu_end(self):
        command = self.view.tournament_menu_end()
        tournament = Tournament.find_by_id(command.choice)
        tournament.change_status(TournamentStatus.TERMINATED)
        print("Le tournoi {} est terminé, félicitation à tous les participants !".format(tournament))

    def add_players_by_ids(self, tournament_id: int, player_list: list[int]):
        for player_id in player_list:
            self.add_player_by_id(tournament_id, player_id)

    def add_player_by_id(self, tournament_id: int, player_id: int):
        tournament = Tournament.find_by_id(tournament_id)
        player = Player.find_by_id(player_id)
        self.add_player(tournament, player)

    def add_player(self, tournament: Tournament, player: Player):
        # on ajoute le joueur a la liste du tournoi
        tournament.add_player_to_tournament(player)
        # on ajoute également le tournoi à la liste de ceux joués par le joueur
        player.add_tournament_to_player(tournament)
        logging.info("Ajout du joueur [{}] au tournoi [{}]".format(player, tournament))
        # TODO afficher la liste des joueurs ajoutés en confirmation


class RoundController():
    view = None
    service = None

    def __init__(self):
        self.view = RoundView()
        self.service = GenerateRoundService()

    def create_round(self, tournament: Tournament) -> Round:
        # ajout date et heure de début du nouveau round
        now = datetime.now()
        tournament.current_round_number += 1
        chess_round = Round(round_number=tournament.current_round_number, start_date=now)
        return chess_round

    def create_first_round(self, tournament: Tournament):
        # on génère un tour
        chess_round = self.create_round(tournament)
        # création des matchs
        chess_round.matchs_list = self.create_matchs(tournament)
        # ajout du round a l'objet tournoi
        self.tournament_add_round(tournament, chess_round)

    def create_next_round(self):
        command = self.view.create_round_menu()
        tournament = Tournament.find_by_id(command.choice)
        # on termine le round précédent
        self.end_round(tournament)
        # puis on génère le nouveau tour
        chess_round = self.create_round(tournament)
        # création des matchs
        chess_round.matchs_list = self.create_matchs(tournament)
        # ajout du round au tournoi
        self.tournament_add_round(tournament, chess_round)

    def tournament_add_round(self, tournament: Tournament, chess_round: Round):
        tournament.rounds_list.append(chess_round)
        print(f"Le {chess_round.round_name} a bien été ajouté")
        logging.info("Ajout du {} au tournoi [{}]".format(chess_round.round_name, tournament))

    def end_round(self, tournament: Tournament):
        # ajout heure de fin du round
        now = datetime.now()
        round = tournament.get_current_round()
        #TODO ajouter round_update(*args)
        round.end_date = now
        tournament.sort_players_by_score()

    def create_matchs(self, tournament: Tournament):
        matchs_list = self.service.create_matchs(tournament)
        return matchs_list

    def add_scores(self):
        # command qui retourne le tournoi et num du tour
        command = self.view.round_menu_current_round()
        tournament = Tournament.find_by_id(command.choice)
        # on récupère la liste des matchs, pour l'afficher
        current_round = tournament.get_current_round()
        new_matchs_list = []
        for match in current_round.matchs_list:
            command = self.view.round_menu_add_scores(match)
            (player1, score1), (player2, score2) = command.match
            tournament.add_score_in_tournament_ranking(score1, player1)
            tournament.add_score_in_tournament_ranking(score2, player2)
            player1.save_matchs_history(tournament, current_round, command.match)
            player2.save_matchs_history(tournament, current_round, command.match)
            new_matchs_list.append(command.match)
            # TODO : ajouter le score au classement du tournoi
        current_round.matchs_list = new_matchs_list


class MatchController():
    def __init__(self) -> None:
        pass

    def create():
        pass

    def check_number_of_players():
        # a ne faire que sur le round ?
        pass
