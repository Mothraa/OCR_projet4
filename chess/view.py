
from chess.model import Tournament, TournamentStatus

import chess.menu_text as text
from chess.command import (MainMenuCommand,
                           PlayerMenuCommand,
                           PlayerCreateCommand,
                           PlayerGenerateCommand,
                           TournamentMenuCommand,
                           TournamentDetailCommand,
                           TournamentCreateCommand,
                           TournamentGenerateCommand,
                           TournamentAddPlayerCommand,
                           TournamentStartCommand,
                           TournamentEndCommand,
                           CreateRoundCommand,
                           TournamentIdCommand,
                           RoundAddScore,
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
        self.main_menu()

    def main_menu(self):
        print(text.MAIN_MENU)

    @InputErrorHandler.catch_input_errors
    def get_user_choice(self):
        choice = input()
        return MainMenuCommand(choice)


class PlayerView(InputErrorHandler):
    def __init__(self) -> None:
        pass

    def player_menu(self):
        print(text.PLAYER_MENU)

    @InputErrorHandler.catch_input_errors
    def get_user_choice(self):
        choice = input()
        return PlayerMenuCommand(choice)

    def display_players(self, players_list):
        print(players_list)

    @InputErrorHandler.catch_input_errors
    def player_create_menu(self):
        print(text.PLAYER_CREATE_MENU)
        last_name = input("Saisir le nom de famille :")
        first_name = input("Saisir le prénom :")
        birthdate = input("Saisir la date de naissance au format AAAA-MM-JJ :")
        return PlayerCreateCommand(last_name=last_name, first_name=first_name, birthdate=birthdate)

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
    def tournament_details_get_tournament_id(self):
        # TODO sortir le print du décorateur
        print(text.TOURNAMENT_DETAIL_MENU)
        tournament_id = input()
        return TournamentDetailCommand(tournament_id)

    def display_tournament_details(self, text: str):
        # TODO
        print(text)

    @InputErrorHandler.catch_input_errors
    def tournament_create_menu(self):
        # TODO sortir le print du décorateur
        print(text.TOURNAMENT_CREATE_MENU)

        name = input("Saisir le nom du tournoi :")
        location = input("Saisir le lieu du tournoi :")
        start_date = input("Saisir la date de début (format AAAA-MM-JJ) :")
        end_date = input("Saisir la date de fin (format AAAA-MM-JJ) :")
        number_of_rounds = input("Saisir le nombre de tours (4 par défaut):")
        description = input("Saisir la description (facultatif) :")

        command = TournamentCreateCommand(name=name,
                                          location=location,
                                          start_date=start_date,
                                          end_date=end_date,
                                          number_of_rounds=number_of_rounds,
                                          description=description,
                                          )
        return command

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

    def tournament_add_players_display(self):
        #TODO
        pass

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
        return TournamentIdCommand(choice)

    @InputErrorHandler.catch_input_errors
    def round_menu_add_scores(self, match):
        (player1, score1), (player2, score2) = match
        print(f"Joueur 1 : {player1}")
        print(f"Joueur 2 : {player2}")
        new_score1 = input("Score du joueur 1 :")
        new_score2 = input("Score du joueur 2 :")
        return RoundAddScore(new_score1, new_score2, match)


class View:
    def tournament_start_round(self):
        View.menu_format("Commencer un tour", type='title')
        tournament_id = View.get_input("ID du tournoi :", int) - 1  # TODO revoir les index pour éviter le -1 ?

        if not Tournament.tournament_repertory[tournament_id].status == TournamentStatus.IN_PROGRESS:
            print("Vous ne pouvez pas commencer un tour sur un tournoi au statut : {}"
                  .format(Tournament.tournament_repertory[tournament_id].status))
            self.tournament_play()
        print("Le tournoi est au tour {}, voulez vous commencer un nouveau tour ?"
              .format(Tournament.tournament_repertory[tournament_id].current_round_number))
        # vérifier si le tournoi est ouvert
        # vérifier si (tous) les matchs du tour précédent ont été joués
        # demander confirmation a l'utilisateur début round x
        # créer le round
        # ajouter une date/heure de début
        # mettre à jour le numero de round courant dans le tournoi
        # générer les couples
        # afficher les couples
        self.tournament_play()

    def tournament_end_round(self):
        View.menu_format("Terminer un tour", type='title')
        tournament_id = View.get_input("ID du tournoi :", int) - 1  # TODO revoir les index pour éviter le -1 ?
        # vérifier si le tournoi est ouvert
        # vérifier si un round à été commencé
        # récupérer l'info du round courant dans le model tournament
        # demander confirmation a l'utilisateur cloture round x
        # ajouter les scores par l'utilisateur
        # ajouter date/heure de fin
