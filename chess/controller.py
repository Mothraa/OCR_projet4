import configparser
import logging
from datetime import datetime
from pprint import pprint

from chess.view import MainView, PlayerView, TournamentView, RoundView, ReportView
from chess.model import Player, Tournament, ChessRound, TournamentStatus
from chess.service import (
                        GeneratePlayerService,
                        GenerateTournamentService,
                        RoundService,
                        ReportService,
                        JsonService,
                        PlayerService,
                        TournamentService,
                        TournamentAddScoreValidate,
                        PlayerCreateValidate,
                        TournamentCreateValidate,
                        TournamentAddPlayerValidate,
                        ReportTournamentDetailsValidate,
                        TournamentStartValidate,
                        TournamentEndValidate,
                        CreateRoundValidate,
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
        logging.basicConfig(level=logging.DEBUG,
                            filename="chess.log",
                            filemode="a",  # "a",
                            encoding='utf-8',
                            format='%(asctime)s - %(levelname)s : %(message)s')  # WARNING
        # change logging level of module Faker (for stop spamming !)
        logging.getLogger('faker').setLevel(logging.ERROR)

        config = configparser.ConfigParser()
        config.read('config.ini')

        MainController.PLAYERS_FILE_PATH = config['Paths']['PLAYERS_FILE_PATH']
        MainController.TOURNAMENTS_FILE_PATH = config['Paths']['TOURNAMENTS_FILE_PATH']

        self.view = MainView()

    def run(self):
        self.json_init()
        self.app_load_data()
        self.main_menu()

    def main_menu(self):
        self.view.main_menu()
        command = self.view.get_user_choice()
        self.main_menu_select(command)

    def json_init(self):
        """initialisation of JSON service and files paths"""
        self.json_service = JsonService()
        # création des fichiers json si inexistants
        self.json_service.create_json_file(MainController.PLAYERS_FILE_PATH)
        self.json_service.create_json_file(MainController.TOURNAMENTS_FILE_PATH)

    def app_load_data(self):
        """load data from JSON files"""
        self.player_service = PlayerService(MainController.PLAYERS_FILE_PATH)
        self.tournament_service = TournamentService(MainController.TOURNAMENTS_FILE_PATH)
        self.json_service.load_app_data()

    def main_menu_select(self, command):
        """App main menu"""
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
        """Main player menu"""
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
            self.main.main_menu()

    def display_players(self):
        """Display players list"""
        players = Player.get_players_repertory()
        self.view.display_players(players)
        # on retourne au menu
        self.player_menu()

    def player_create_menu(self):
        command = self.view.player_create_menu()
        PlayerCreateValidate.validate(command.national_chess_id, command.birthdate)
        self.player_create(command.to_dict())
        self.player_menu()

    def players_generate(self):
        command = self.view.player_generate_menu()
        for _ in range(command.choice):
            command_player = self.generate_player_service.generate_player_all_attrs()
            self.player_create(command_player)
        self.player_menu()

    def player_create(self, command):
        player = Player(**command)
        self.player_service.add_player_as_json(player)
        print("création du joueur >> " + str(player))
        logging.info("création du joueur >> " + str(player))


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
        """Main tournament menu"""
        self.view.tournament_menu()
        command = self.view.tournament_menu_user_choice()
        self.tournament_menu_select(command)

    def tournament_menu_select(self, command):
        if command.choice == 1:
            self.display_tournaments()
        elif command.choice == 2:
            self.tournament_menu_create()
        elif command.choice == 3:
            self.tournament_generate()
        elif command.choice == 4:
            self.tournament_add_players()
        elif command.choice == 5:
            self.tournament_menu_start()
        elif command.choice == 6:
            self.tournament_menu_add_scores()
        elif command.choice == 7:
            self.tournament_menu_continue()
        elif command.choice == 8:
            self.tournament_menu_end()
        elif command.choice == 9:
            self.main.main_menu()

    def display_tournaments(self):
        tournaments = Tournament.tournaments_repertory
        self.view.display_tournaments(tournaments)
        self.tournament_menu()

    def tournament_menu_create(self):
        command = self.view.tournament_create_menu()
        TournamentCreateValidate.validate(command.start_date, command.end_date)
        self.tournament_create(command.to_dict())
        self.tournament_menu()

    def tournament_generate(self):
        command = self.view.tournament_generate_menu()
        for _ in range(command.choice):
            command_tournament = self.generate_service.generate_tournament_all_attrs()
            self.tournament_create(command_tournament)
        self.tournament_menu()

    def tournament_create(self, command):
        tournament = Tournament(**command)
        self.tournament_service.add_tournament_as_json(tournament)
        print("création d'un tournoi >> " + str(tournament))
        logging.info("création d'un tournoi >> " + str(tournament))
        return tournament

    def tournament_add_players(self):
        command = self.view.tournament_add_players()
        TournamentAddPlayerValidate.validate(command.tournament_id, command.players_id_list)
        self.add_players_by_ids(command.tournament_id, command.players_id_list)
        tournament = Tournament.find_by_id(command.tournament_id)
        self.tournament_service.update_tournament_as_json(tournament)
        self.tournament_menu()

    def tournament_menu_start(self):
        command = self.view.tournament_menu_start()
        TournamentStartValidate.validate(command.choice)
        tournament = Tournament.find_by_id(command.choice)
        self.tournament_init(tournament)
        self.tour.create_first_round(tournament)
        self.tournament_service.update_tournament_as_json(tournament)
        self.tournament_menu()

    def tournament_menu_add_scores(self):
        tournament = self.tour.add_scores()
        self.tournament_service.update_tournament_as_json(tournament)
        for player in tournament.player_score_list:
            player_id, _ = player
            player_instance = Player.find_by_id(player_id)
            self.player_service.update_player_as_json(player_instance)
        self.tournament_menu()

    def tournament_init(self, tournament: Tournament):
        tournament.current_round_number = 0
        tournament.change_status(TournamentStatus.IN_PROGRESS)

    def tournament_menu_continue(self):
        tournament = self.tour.create_next_round()
        self.tournament_service.update_tournament_as_json(tournament)
        self.tournament_menu()

    def tournament_menu_end(self):
        command = self.view.tournament_menu_end()
        TournamentEndValidate.validate(command.choice)
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
        player.tournaments_history = tournament.id
        self.player_service.update_player_as_json(player)
        pprint("Ajout du joueur [{}] au tournoi [{}]".format(player, tournament.name), indent=4)
        logging.info("Ajout du joueur [{}] au tournoi [{}]".format(player, tournament))


class RoundController():
    view = None
    round_service = None

    def __init__(self):
        self.view = RoundView()
        self.round_service = RoundService()

    def create_round(self, tournament: Tournament) -> ChessRound:
        """Create a round of Tournament"""
        tournament.current_round_number += 1
        chess_round = ChessRound(id=tournament.current_round_number,
                                 round_name=f"Tour {tournament.current_round_number}",
                                 )
        # ajout date et heure de début du nouveau round
        chess_round.start_date = datetime.now()
        return chess_round

    def create_first_round(self, tournament: Tournament):
        """Create the first round of a tournament"""
        # on génère un tour
        chess_round = self.create_round(tournament)
        # création des matchs
        matchs_list_to_add = self.create_matchs(tournament)
        chess_round.matchs_list = matchs_list_to_add
        # chess_round.add_matchs(matchs_list)
        # ajout du round a l'objet tournoi
        self.tournament_add_round(tournament, chess_round)

    def create_next_round(self):
        """End a round and start a new one"""
        command = self.view.create_round_menu()
        CreateRoundValidate.validate(command.choice)
        tournament = Tournament.find_by_id(command.choice)
        # on termine le round précédent
        self.end_round(tournament)
        # puis on génère le nouveau tour
        chess_round = self.create_round(tournament)
        # création des matchs
        matchs_list_to_add = self.create_matchs(tournament)
        chess_round.matchs_list = matchs_list_to_add
        # chess_round.add_matchs(matchs_list)
        # ajout du round au tournoi
        self.tournament_add_round(tournament, chess_round)
        return tournament

    def tournament_add_round(self, tournament: Tournament, chess_round: ChessRound):
        tournament.rounds_list.append(chess_round)
        print(f"Le {chess_round.round_name} a bien été ajouté")
        logging.info("Ajout du {} au tournoi [{}]".format(chess_round.round_name, tournament))

    def end_round(self, tournament: Tournament):
        """Complete a Round"""
        # ajout heure de fin du round
        chess_round = tournament.current_round()
        chess_round.end_date = datetime.now()

        print(f"fin du {chess_round.round_name}")
        logging.info(f"fin du {chess_round.round_name} du tournoi {tournament}")
        tournament.sort_players_by_score()

    def create_matchs(self, tournament: Tournament):
        """Generate matchs (associate players)"""
        matchs_list = self.round_service.create_matchs(tournament)
        return matchs_list

    def add_scores(self):
        """Add scores to the current Round"""
        command = self.view.round_menu_current_round()
        TournamentAddScoreValidate.validate(command.choice)
        tournament = Tournament.find_by_id(command.choice)
        print("Ajout du score pour le tournoi {} // Tour : {} sur {}".format(tournament,
                                                                             tournament.current_round_number,
                                                                             tournament.number_of_rounds,
                                                                             ))
        self.round_service.add_scores_to_tournament(tournament, self.view.round_menu_add_scores)
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
            self.main.main_menu()

    def report_all_players(self):
        """Show players list in alphabetical order"""
        player_list = Player.get_players_repertory()
        player_list_sorted = ReportService.sort_players_list_by_name(player_list)
        pprint(player_list_sorted, indent=4)
        self.report_menu()
        # for player in players_list:
        #     print(player.encode())

    def report_all_tournaments(self):
        """Show tournaments list"""
        pprint(Tournament.tournaments_repertory, indent=4)
        self.report_menu()

    def report_tournament_details(self):
        """Show details of one tournament"""
        command = self.view.report_tournament_details()
        ReportTournamentDetailsValidate.validate(command.choice)
        tournament = Tournament.find_by_id(command.choice)
        tournament_dict = ReportService.tournament_details(tournament)
        pprint(tournament_dict)
        self.report_menu()
