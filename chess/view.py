import logging

from datetime import date

from chess.controller import Controller, InputManagement
from chess.model import Player, Tournament
from chess.generator import Creator


class View:

    def __init__(self):
        self.controller = Controller()
        self.createur = Creator()
        # controller.run()

    def main_menu(self):

        View.menu_format("Application d'échec",
                         "Menu principal",
                         type='title'
                         )
        # TODO : utiliser enumerate pour la numérotation ?
        View.menu_format("Gestion joueurs",
                         "Gestion Tournois",
                         "Jouer un tournoi",
                         type='choice'
                         )

        View.menu_input(self.menu_player, self.menu_tournament, self.tournament_play)

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

    @staticmethod
    def menu_input(* args):

        num_quit = len(args) + 1

        choix = None
        while choix not in range(1, num_quit + 1):
            try:
                choix = int(input("Choix : "))
            except ValueError:
                print("Merci de saisir un numéro.")
            except IndexError:
                print("Merci de saisir un numéro valide.")
            except Exception as e:
                print(e)

        if choix == num_quit:
            return print("A bientôt !")

        logging.debug("choix menu >> " + str(args[choix - 1]))
        args[choix - 1]()

    @staticmethod
    def get_input(input_message: str, *args: type) -> any:
        while True:
            input_value = input(input_message)
            if InputManagement.check_input(input_value, *args):
                # TODO a refactoriser
                for input_type in args:
                    if isinstance(int(input_value), int):
                        input_value = int(input_value)
                return input_value

    def menu_player(self):
        View.menu_format("Menu joueurs", type='title')
        View.menu_format("Création joueur",
                         "Génération joueur (POUR TEST UNIQUEMENT)",
                         "Retour au menu principal",
                         type='choice'
                         )
        View.menu_input(self.player_create, self.player_generate, self.main_menu)

    def menu_tournament(self):
        View.menu_format("Menu tournois", type='title')
        View.menu_format("Afficher la liste des tournois",
                         "Nouveau tournoi",
                         "Génération tournoi (POUR TEST UNIQUEMENT)",
                         "Modifier Tournoi",
                         "Menu principal",
                         type='choice'
                         )
        View.menu_input(self.tournament_show_all,
                        self.tournament_create,
                        self.tournament_generate,
                        self.tournament_modify,
                        self.main_menu
                        )

    def player_create(self):
        View.menu_format("Création joueur", type='title')
        last_name = View.get_input("Saisir le nom de famille :", str)
        first_name = View.get_input("Saisir le prénom :", str)
        birthdate = View.get_input("Saisir la date de naissance au format AAAA-MM-JJ :", date)
        # TODO : ajouter les autres inputs
        self.controller.manage_player.create(last_name=last_name, first_name=first_name, birthdate=birthdate)
        # on retourne sur le menu précédent
        self.menu_player()

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
        number_of_rounds = View.get_input("Nombre tours (4 par défaut) :", int)  # type(None))
        description = View.get_input("Description :", str)
        tournoi = self.controller.manage_tournament.create(name=name,
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

    def tournament_add_player(self):
        View.menu_format("Ajouter des joueurs au tournoi", type='title')
        repertory_tournament = Tournament.get_tournament_repertory()
        tournament_id = View.get_input("ID du tournoi à modifier :", int) - 1  # TODO revoir les index pour éviter le -1 ?

        print("Tournoi : " + str(repertory_tournament[tournament_id]))
        print("Liste joueurs : " + str(Player.get_player_repertory()))
        print("indiquez un ou plusieurs ID de joueurs séparés par des espaces")

        players_id_list = (input("Choix ID Joueurs :")).strip().split(sep=" ")
        # TODO revoir les index pour éviter le -1 ?
        players_id_list = [InputManagement.check_input(player_id, int) - 1 for player_id in players_id_list]
        self.controller.manage_tournament.add_players_from_ids(tournament_id, players_id_list)
        self.menu_tournament()

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
                         "Démarrer un nouveau round",
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
        repertory_tournament = Tournament.get_tournament_repertory()
        tournament_id = View.get_input("ID du tournoi :", int) - 1  # TODO revoir les index pour éviter le -1 ?
        print("Tournoi : " + str(repertory_tournament[tournament_id]))

        self.tournament_play()

    def tournament_start(self):
        pass

    def tournament_start_round(self):
        # saisie de l'id du tournoi par l'utilisateur
        # créer le round
        # ajouter une date/heure de début
        # mettre à jour le round courant dans le tournoi
        # générer les couples


    def tournament_end_round(self):
        # saisie de l'id du tournoi par l'utilisateur
        # récupérer l'info du round courant dans le model tournament
        # ajouter date/heure de fin
        # ajouter les scores par l'utilisateur
