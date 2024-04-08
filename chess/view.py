
#from chess.controller import Controller, InputManagement
from chess.model import Player, Tournament, TournamentStatus
#from chess.service import Creator
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
                           PlayersToAddInTournamentCommand,
                           TournamentStartCommand,
                           CreateRoundCommand,
                           )

# # exemple de décorateur a généraliser pour get_user_choice()
# class InputErrorHandler:
#     @staticmethod
#     def catch_input_errors(func):
#         def wrapper(*args, **kwargs):
#             while True:
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception as e:
#                     print(e)
#         return wrapper
#         logging.debug("choix menu >> " + str(args[choix - 1]))

# class MainView(InputErrorHandler):
#     @InputErrorHandler.catch_input_errors
#     def get_user_choice(self):
#         choice = input()
#         return TournamentMenuCommand(choice)


class MainView:
    def __init__(self):
        self.main_menu()

    def main_menu(self):
        print(text.MAIN_MENU)

    def get_user_choice(self):
        while True:
            try:
                choice = input()
                return MainMenuCommand(choice)
            except Exception as e:
                print(e)


class PlayerView:
    def __init__(self) -> None:
        pass

    def player_menu(self):
        print(text.PLAYER_MENU)

    def get_user_choice(self):
        while True:
            try:
                choice = input()
                return PlayerMenuCommand(choice)
            except Exception as e:
                print(e)

    def display_players(self, players_list):
        print(players_list)

    def player_create_menu(self):
        print(text.PLAYER_CREATE_MENU)
        while True:
            try:
                last_name = input("Saisir le nom de famille :")
                first_name = input("Saisir le prénom :")
                birthdate = input("Saisir la date de naissance au format AAAA-MM-JJ :")

                command = PlayerCreateCommand(last_name=last_name, first_name=first_name, birthdate=birthdate)
                return command
            except Exception as e:
                print(e)

    def player_generate_menu(self):
        while True:
            try:
                print(text.PLAYER_GENERATE_MENU)
                choice = input()
                return PlayerGenerateCommand(choice)
            except Exception as e:
                print(e)


class TournamentView:
    def __init__(self) -> None:
        pass

    def tournament_menu(self):
        print(text.TOURNAMENT_MENU)

    def tournament_menu_user_choice(self):
        while True:
            try:
                choice = input()
                return TournamentMenuCommand(choice)
            except Exception as e:
                print(e)

    def display_tournaments(self, tournaments_list):
        print(tournaments_list)

    def tournament_details_get_tournament_id(self):
        print(text.TOURNAMENT_DETAIL_MENU)
        while True:
            try:
                tournament_id = input()
                return TournamentDetailCommand(tournament_id)
            except Exception as e:
                print(e)

    def display_tournament_details(self, text: str):
        print(text)

    def tournament_create_menu(self):
        print(text.TOURNAMENT_CREATE_MENU)
        while True:
            try:
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
            except Exception as e:
                print(e)

    def tournament_generate_menu(self):
        print(text.TOURNAMENT_GENERATE_MENU)
        while True:
            try:
                tournament_number = input()
                return TournamentGenerateCommand(tournament_number)
            except Exception as e:
                print(e)

    def tournament_add_players_get_tournament_id(self):
        print(text.TOURNAMENT_ADD_PLAYERS_MENU)
        while True:
            try:
                tournament_id = input()
                return TournamentAddPlayerCommand(tournament_id)
            except Exception as e:
                print(e)

    def tournament_add_players_get_players_id(self):
        print(text.TOURNAMENT_ADD_PLAYERS_LIST)
        while True:
            try:
                players_id = input()
                return PlayersToAddInTournamentCommand(players_id)
            except Exception as e:
                print(e)

    def tournament_add_players_display(self):
        #TODO
        pass

    def tournament_menu_start(self):
        print(text.TOURNAMENT_START_MENU)
        while True:
            try:
                choice = input()
                return TournamentStartCommand(choice)
            except Exception as e:
                print(e)


class RoundView:
    def __init__(self):
        pass

    def create_round_menu(self):
        print(text.ROUND_MENU)
        tournament_choice = input()
        return CreateRoundCommand(tournament_choice)


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
