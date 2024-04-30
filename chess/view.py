import chess.menu_text as text
from chess.command import (MainMenuCommand,
                           PlayerMenuCommand,
                           PlayerCreateCommand,
                           PlayerGenerateCommand,
                           TournamentMenuCommand,
                           TournamentCreateCommand,
                           TournamentGenerateCommand,
                           TournamentAddPlayerCommand,
                           TournamentStartCommand,
                           TournamentEndCommand,
                           CreateRoundCommand,
                           TournamentAddScoreCommand,
                           RoundAddScoreCommand,
                           ReportMenuCommand,
                           ReportTournamentDetailsCommand,
                           )


class InputErrorHandler:
    @staticmethod
    def catch_input_errors(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
        return wrapper


class MainView(InputErrorHandler):
    def __init__(self):
        pass

    def main_menu(self):
        print(text.MAIN_MENU)

    @InputErrorHandler.catch_input_errors
    def get_user_choice(self):
        choice = input()
        return MainMenuCommand(choice)


class PlayerView(InputErrorHandler):
    def __init__(self) -> None:
        pass

    @InputErrorHandler.catch_input_errors
    def player_menu(self):
        print(text.PLAYER_MENU)
        choice = input()
        return PlayerMenuCommand(choice)

    def display_players(self, players_list):
        print(players_list)

    @InputErrorHandler.catch_input_errors
    def player_create_menu(self):
        print(text.PLAYER_CREATE_MENU)
        national_chess_id = input("Saisir l'ID National (2 lettres majuscules + 5 chiffres) :")
        last_name = input("Saisir le nom de famille :")
        first_name = input("Saisir le prénom :")
        birthdate = input("Saisir la date de naissance au format AAAA-MM-JJ :")
        return PlayerCreateCommand(national_chess_id=national_chess_id,
                                   last_name=last_name,
                                   first_name=first_name,
                                   birthdate=birthdate,
                                   )

    @InputErrorHandler.catch_input_errors
    def player_generate_menu(self):
        print(text.PLAYER_GENERATE_MENU)
        choice = input()
        return PlayerGenerateCommand(choice)


class TournamentView(InputErrorHandler):
    def __init__(self) -> None:
        pass

    def tournament_menu(self):
        print(text.TOURNAMENT_MENU)

    @InputErrorHandler.catch_input_errors
    def tournament_menu_user_choice(self):
        choice = input()
        return TournamentMenuCommand(choice)

    def display_tournaments(self, tournaments_list):
        print(tournaments_list)

    @InputErrorHandler.catch_input_errors
    def tournament_create_menu(self):
        print(text.TOURNAMENT_CREATE_MENU)

        name = input("Saisir le nom du tournoi :")
        location = input("Saisir le lieu du tournoi :")
        start_date = input("Saisir la date de début (format AAAA-MM-JJ) :")
        end_date = input("Saisir la date de fin (format AAAA-MM-JJ) :")
        number_of_rounds = input("Saisir le nombre de tours (4 par défaut):")
        description = input("Saisir la description (facultatif) :")

        tournament_data = {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "number_of_rounds": number_of_rounds,
            "description": description
        }

        # command = TournamentCreateCommand(name=name,
        #                                   location=location,
        #                                   start_date=start_date,
        #                                   end_date=end_date,
        #                                   number_of_rounds=number_of_rounds,
        #                                   description=description,
        #                                   )
        return TournamentCreateCommand(**tournament_data)

    @InputErrorHandler.catch_input_errors
    def tournament_generate_menu(self):
        print(text.TOURNAMENT_GENERATE_MENU)
        tournament_number = input()
        return TournamentGenerateCommand(tournament_number)

    @InputErrorHandler.catch_input_errors
    def tournament_add_players(self):
        print(text.TOURNAMENT_ADD_PLAYERS_MENU)
        tournament_id = input()
        print(text.TOURNAMENT_ADD_PLAYERS_LIST)
        players_id_list = input()
        return TournamentAddPlayerCommand(tournament_id, players_id_list)

    @InputErrorHandler.catch_input_errors
    def tournament_menu_start(self):
        print(text.TOURNAMENT_START_MENU)
        choice = input()
        return TournamentStartCommand(choice)

    @InputErrorHandler.catch_input_errors
    def tournament_menu_end(self):
        print(text.TOURNAMENT_END_MENU)
        choice = input()
        return TournamentEndCommand(choice)


class RoundView(InputErrorHandler):
    def __init__(self):
        pass

    @InputErrorHandler.catch_input_errors
    def create_round_menu(self):
        print(text.ROUND_MENU)
        tournament_choice = input()
        return CreateRoundCommand(tournament_choice)

    @InputErrorHandler.catch_input_errors
    def round_menu_current_round(self):
        print(text.ROUND_MENU_ADD_SCORES)
        choice = input()
        return TournamentAddScoreCommand(choice)

    @InputErrorHandler.catch_input_errors
    def round_menu_add_scores(self, player1, player2, match):
        print(f"Joueur 1 : {player1}")
        print(f"Joueur 2 : {player2}")
        new_score1 = input("Score du joueur 1 :")
        new_score2 = input("Score du joueur 2 :")
        return RoundAddScoreCommand(new_score1, new_score2, match)


class ReportView(InputErrorHandler):
    def __init__(self):
        pass

    @InputErrorHandler.catch_input_errors
    def create_report_menu(self):
        print(text.REPORT_MENU)
        choice = input()
        return ReportMenuCommand(choice)

    def report_tournament_details(self):
        print(text.REPORT_TOURNAMENT_DETAILS)
        choice = input()
        return ReportTournamentDetailsCommand(choice)
