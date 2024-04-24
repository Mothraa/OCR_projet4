from datetime import datetime
from pprint import pprint
import os
import configparser
import logging

from chess.view import MainView, PlayerView, TournamentView, RoundView, ReportView
from chess.model import Player, Tournament, Round, TournamentStatus
from chess.service import (
                        GeneratePlayerService,
                        GenerateTournamentService,
                        RoundService,
                        ReportService,
                        JsonService,
                        PlayerService,
                        TournamentService,
                        )


class MainController():
    config = None
    PLAYERS_FILE_PATH = None
    TOURNAMENTS_FILE_PATH = None
    view = None
    json_service = None
    player_service = None
    tournament_service = None

    def __init__(self) -> None:
        # logging a passer en singleton pour pouvoir l'appeler partout ?
        logging.basicConfig(level=logging.DEBUG,
                            filename="chess.log",
                            filemode="a",  # "a",
                            encoding='utf-8',
                            format='%(asctime)s - %(levelname)s : %(message)s')  # WARNING
        # pour eviter que faker nous spam de logs
        logging.getLogger('faker').setLevel(logging.ERROR)

        config = configparser.ConfigParser()
        config.read('config.ini')

        MainController.PLAYERS_FILE_PATH = config['Paths']['PLAYERS_FILE_PATH']
        MainController.TOURNAMENTS_FILE_PATH = config['Paths']['TOURNAMENTS_FILE_PATH']

        self.view = MainView()

    def run(self):
        self.json_init()
        self.app_load_data()

        self.view.main_menu()
        command = self.view.get_user_choice()
        self.main_menu_select(command)
        # logging.warning("whoaa!")
        # init json

    def json_init(self):
        self.json_service = JsonService()
        # création des fichiers json si inexistants
        self.json_service.create_json_file(MainController.PLAYERS_FILE_PATH)
        self.json_service.create_json_file(MainController.TOURNAMENTS_FILE_PATH)

    def app_load_data(self):
        self.player_service = PlayerService(MainController.PLAYERS_FILE_PATH)
        self.tournament_service = TournamentService(MainController.TOURNAMENTS_FILE_PATH)
        self.json_service.load_app_data()

    def main_menu_select(self, command):
        if command.choice == 1:
            PlayerController(MainController.PLAYERS_FILE_PATH)
        elif command.choice == 2:
            TournamentController(tournament_file_path=MainController.TOURNAMENTS_FILE_PATH,
                                 player_file_path=MainController.PLAYERS_FILE_PATH,
                                 )
        elif command.choice == 3:
            ReportController()
        elif command.choice == 4:
            print("bye !")


class PlayerController():
    view = None
    player_service = None
    main = None
    json_service = None
    generate_player_service = None

    def __init__(self, player_file_path) -> None:
        player_file_path
        self.view = PlayerView()
        self.main = MainController()
        self.player_service = PlayerService(player_file_path)
        self.json_service = JsonService()
        self.generate_player_service = GeneratePlayerService()

        self.player_menu()

    def player_menu(self):
        command = self.view.player_menu()
        self.player_menu_select(command)

    def player_menu_select(self, command):
        if command.choice == 1:
            self.display_players()
        elif command.choice == 2:
            self.player_create_menu()
        elif command.choice == 3:
            self.players_generate()
        elif command.choice == 4:
            self.main.run()

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
        self.player_service.add_player_as_json(player)
        logging.info("création du joueur >> " + str(player))

    def players_generate(self):
        command = self.view.player_generate_menu()

        for _ in range(command.choice):
            command_player = self.generate_player_service.generate_player_all_attrs()
            self.player_create(command_player)
        #     player_list.append(player)
        # return player_list
        # self.generateur.add_players_all_attrs(command)
        # on retourne au menu
        self.player_menu()


class TournamentController():
    view = None
    tour = None
    json_service = None
    tournament_service = None
    player_service = None
    tournament_generate_service = None
    main = None

    def __init__(self, tournament_file_path, player_file_path) -> None:
        self.view = TournamentView()
        self.tour = RoundController()
        self.json_service = JsonService()
        self.tournament_service = TournamentService(tournament_file_path)
        self.player_service = PlayerService(player_file_path)
        self.generate_service = GenerateTournamentService()
        self.main = MainController()

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
            self.main.run()

    def display_tournaments(self):
        tournaments = Tournament.get_tournaments_repertory()
        self.view.display_tournaments(tournaments)
        # on retourne au menu
        self.tournament_menu()

    def display_tournament_details(self):
        # command = self.view.tournament_details_get_tournament_id()
        # Tournament.find_by_id(command.choice)
        # TODO 'nécessite de finir la serialisation de l'objet en text / json
        self.tournament_menu()

    def tournament_menu_create(self):
        command = self.view.tournament_create_menu()
        self.tournament_create(command)
        # on retourne au menu
        self.tournament_menu()

    def tournament_create(self, command):
        # tournament = Tournament(
        #                           name=command.name,
        #                           location=command.location,
        #                           start_date=command.start_date,
        #                           end_date=command.end_date,
        #                           description=command.description,
        #                           number_of_rounds=command.number_of_rounds
        #                           )
        tournament = Tournament(**command)
        self.tournament_service.add_tournament_as_json(tournament)
        logging.info("création d'un tournoi >> " + str(tournament))
        return tournament

    def tournament_generate(self):
        command = self.view.tournament_generate_menu()
        for _ in range(command.choice):
            command_tournament = self.generate_service.generate_tournament_all_attrs()
            # trier par date de début avant création ?
            self.tournament_create(command_tournament)
        self.tournament_menu()

    def tournament_add_players(self):
        # TODO : ajouter controle
        command = self.view.tournament_add_players()
        self.add_players_by_ids(command.tournament_id, command.players_id_list)
        # TODO afficher le resultat
        tournament = Tournament.find_by_id(command.tournament_id)
        self.tournament_service.update_tournament_as_json(tournament)

        self.tournament_menu()

    def tournament_menu_start(self):
        # TODO : ajouter controle
        command = self.view.tournament_menu_start()
        tournament = Tournament.find_by_id(command.choice)
        self.tournament_init(tournament)
        self.tour.create_first_round(tournament)
        self.tournament_service.update_tournament_as_json(tournament)
        self.tournament_menu()

    def tournament_menu_add_scores(self):
        # TODO : ajouter controle
        tournament = self.tour.add_scores()
        self.tournament_service.update_tournament_as_json(tournament)
        self.tournament_menu()

    def tournament_init(self, tournament: Tournament):
        tournament.current_round_number = 0
        tournament.change_status(TournamentStatus.IN_PROGRESS)

    def tournament_menu_continue(self):
        # TODO : ajouter controle
        tournament = self.tour.create_next_round()
        self.tournament_service.update_tournament_as_json(tournament)
        self.tournament_menu()

    def tournament_menu_end(self):
        # TODO : ajouter controle
        command = self.view.tournament_menu_end()
        tournament = Tournament.find_by_id(command.choice)
        tournament.change_status(TournamentStatus.TERMINATED)
        self.tournament_service.update_tournament_as_json(tournament)
        print("Le tournoi {} est terminé, félicitation à tous les participants !".format(tournament))
        self.tournament_menu()

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
        player.set_tournament_history(tournament)
        self.player_service.update_player_as_json(player)
        logging.info("Ajout du joueur [{}] au tournoi [{}]".format(player, tournament))


class RoundController():
    view = None
    round_service = None

    def __init__(self):
        self.view = RoundView()
        self.round_service = RoundService()

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
        return tournament

    def tournament_add_round(self, tournament: Tournament, chess_round: Round):
        tournament.rounds_list.append(chess_round)
        print(f"Le {chess_round.round_name} a bien été ajouté")
        #TODO maj tournoi json
        logging.info("Ajout du {} au tournoi [{}]".format(chess_round.round_name, tournament))


    def end_round(self, tournament: Tournament):
        # ajout heure de fin du round
        now = datetime.now()
        round = tournament.get_current_round()
        # TODO ajouter round_update(*args)
        round.end_date = now
        tournament.sort_players_by_score()

    def create_matchs(self, tournament: Tournament):
        matchs_list = self.round_service.create_matchs(tournament)
        return matchs_list

    def add_scores(self):
        # TODO : gérer l'erreur si on souhaite ajouter les scores sans avoir commencé le tournoi
        # command qui retourne l'ID du tournoi
        command = self.view.round_menu_current_round()
        # self.round_service.add_scores(command.choice)
        tournament = Tournament.find_by_id(command.choice)
        # on récupère le tour courant (contenant la liste des matchs)
        current_round = tournament.get_current_round()
        new_matchs_list = []
        for match in current_round.matchs_list:
            # TODO a revoir
            (player1_id, _), (player2_id, _) = match
            player1 = Player.find_by_id(player1_id)
            player2 = Player.find_by_id(player2_id)
            # TODO regrouper player1, 2 dans match ?
            command = self.view.round_menu_add_scores(player1, player2, match)
            (player1_id, score1), (player2_id, score2) = command.match
            # tournament.add_score_in_tournament_ranking(score1, player1_id)
            # tournament.add_score_in_tournament_ranking(score2, player2_id)
            self.round_service.add_score_in_tournament_ranking(tournament, score1, player1_id)
            self.round_service.add_score_in_tournament_ranking(tournament, score2, player2_id)

            player1.set_matchs_history(tournament, current_round, command.match)
            player2.set_matchs_history(tournament, current_round, command.match)
            # TODO : update json player1 et player2
            new_matchs_list.append(command.match)
            # TODO : ajouter le score au classement du tournoi
        current_round.matchs_list = new_matchs_list
        return tournament


class ReportController():
    view = None
    service = None
    main = None

    def __init__(self) -> None:
        self.view = ReportView()
        self.main = MainController()
        self.report_menu()

    def report_menu(self):
        command = self.view.create_report_menu()
        self.report_menu_select(command)

    def report_menu_select(self, command):
        if command.choice == 1:
            self.report_all_players()
        elif command.choice == 2:
            self.report_all_tournaments()
        elif command.choice == 3:
            self.report_tournament_details()
        elif command.choice == 4:
            self.main.run()

    def report_all_players(self):
        # liste de tous les joueurs par ordre alphabétique
        player_list = Player.get_players_repertory()
        player_list_sorted = ReportService.sort_players_list_by_name(player_list)
        pprint(player_list_sorted, indent=4)
        self.report_menu()
        # for player in players_list:
        #     print(player.encode())

    def report_all_tournaments(self):
        # liste de tous les tournois
        pprint(Tournament.get_tournaments_repertory(), indent=4)
        self.report_menu()

    def report_tournament_details(self):
        command = self.view.report_tournament_details()
        tournament = Tournament.find_by_id(command.choice)
        tournament_dict = ReportService.tournament_details(tournament)
        pprint(tournament_dict)
        # nom et dates d’un tournoi donné
        # liste des joueurs du tournoi par ordre alphabétique
        # liste de tous les tours du tournoi et de tous les matchs du tour.
        self.report_menu()
