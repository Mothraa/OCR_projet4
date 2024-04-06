import logging

from datetime import date

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

    def generate_round_menu(self):
        print(text.ROUND_MENU)
        tournament_code = int(input())
        return GenerateRoundCommand(tournament_code)


class View:


    @staticmethod
    def menu_format(*args, type):
        NB_AJOUT_ESPACES = 10

        if type == "title":

            max_len = 0
            for texte in args:
                if max_len < len(texte):
                    max_len = len(texte)
            max_len = max_len + NB_AJOUT_ESPACES
            # on traite le cas ou le nombre est impair (pb de centrage)
            if (max_len % 2) != 0:
                max_len += 1

            print("*" * max_len)
            print("*" + " " * (max_len - 2) + "*")
            for texte in args:
                len_espace = max_len - len(texte) - 2
                espace = int(len_espace / 2)

                if (len_espace % 2) != 0:
                    # on ajoute un espace en plus a la fin si impaire
                    texte_temp = "*" + " " * espace + texte + " " * espace + " *"
                else:
                    texte_temp = "*" + " " * espace + texte + " " * espace + "*"
                print(texte_temp)

            print("*" + " " * (max_len - 2) + "*")
            print("*" * max_len)

        elif type == "choice":
            for i, texte in enumerate(args, 1):
                print(str(i) + " - " + texte)
            # print("Tapez le numéro de l'option souhaitée :")
            # ajoute par défaut l'option pour quitter a tous les menus
            print(str(len(args) + 1) + " - Quitter")


    def player_generate(self):
        nb_players = View.get_input("Nombre de joueurs à créer :", int)
        self.createur.player(nb_players)
        print("Génération des joueurs : " + str(Player.get_player_repertory()))
        # on retourne sur le menu précédent
        self.menu_player()

    def tournament_create(self):
        View.menu_format("Création d'un tournoi", type='title')
        name = View.get_input("Nom du tournoi :", str)
        location = View.get_input("lieu :", str)
        start_date = View.get_input("date début (format AAA/MM/JJ) :", date)
        end_date = View.get_input("date fin (format AAA/MM/JJ) :", date)
        # TODO ajouter le None
        number_of_rounds = View.get_input("Nombre tours (4 par défaut) :", int) # type(None))
        description = View.get_input("Description :", str)
        # tournoi = self.controller.manage_tournament.create(name=name,
        self.controller.manage_tournament.create(name=name,
                                                 location=location,
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 number_of_rounds=number_of_rounds,
                                                 description=description,
                                                 )
        # on retourne sur le menu précédent
        self.menu_tournament()

    def tournament_generate(self):
        nb_tournaments = View.get_input("Saisir le nombre de tournois à générer :", int)
        self.createur.tournament(nb_tournaments)
        print("Génération des tournois : " + str(Tournament.get_tournament_repertory()))
        # on retourne sur le menu précédent
        self.menu_tournament()

    def tournament_show_all(self):
        print("Tournois : " + str(Tournament.get_tournament_repertory()))
        self.menu_tournament()

    def tournament_modify(self):
        View.menu_format("Modification d'un tournoi", type='title')
        View.menu_format("Ajouter des joueurs à un tournoi",
                         # "Modifier les informations d'un tournoi",
                         ""
                         "Retour au menu principal",
                         type='choice'
                         )
        View.menu_input(self.tournament_add_player,
                        # self.tournament_modify_infos,
                        self.main_menu,
                        )
        # self.menu_tournament()

    def tournament_modify_infos(self, tournament_id: int):
        print("Informations du tournoi selectionné, entrer pour passer sans modifier")

        # name = input("Nom du tournoi > ")
        # location = input("lieu > ")
        # start_date = input("date début (format AAA/MM/JJ) > ")
        # end_date = input("date fin (format AAA/MM/JJ) > ")
        # number_of_rounds = input("Nombre tours (4 par défaut) > ")
        # description = input("Description > ")

        self.menu_tournament()

    def tournament_play(self):
        View.menu_format("Informations sur un tournoi",
                         "Démarrer un tournoi",
                         "Commencer un tour",
                         "Terminer un round",
                         # "Ajouter un round",
                         "Retour au menu principal",
                         type='choice'
                         )

        View.menu_input(self.tournament_infos,
                        self.tournament_start,
                        self.tournament_start_round,
                        self.tournament_end_round,
                        # self.tournament_add_round,
                        self.main_menu,
                        )

    def tournament_infos(self):
        View.menu_format("Informations sur un tournoi", type='title')
        tournament_repertory = Tournament.get_tournament_repertory()
        tournament_id = View.get_input("ID du tournoi :", int) - 1  # TODO revoir les index pour éviter le -1 ?
        print("Tournoi : " + str(tournament_repertory[tournament_id]))

        self.tournament_play()

    def tournament_start(self):
        View.menu_format("Commencer un tournoi", type='title')
        tournament_id = View.get_input("ID du tournoi :", int) - 1  # TODO revoir les index pour éviter le -1 ?
        # TODO : instancier le tournoi ou récup juste dans la liste ?
        # ajouter statut début tournoi
        Tournament.tournament_repertory[tournament_id].status = TournamentStatus.IN_PROGRESS
        # ajouter une date/heure de début du tournoi <= non spécifié, on utilise les dates renseignées à la création
        print("Début du tournoi : {}\n"
              .format(Tournament.tournament_repertory[tournament_id])
              + "Le tournoi est en {} tour(s).\n"
              .format(Tournament.tournament_repertory[tournament_id].number_of_rounds)
              + "Merci de débuter un tour")
        self.tournament_play()

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

