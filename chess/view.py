from chess.controller import Controller
from chess.model import Player, Tournament
from chess.generator import Creator


class View:

    def __init__(self):
        self.controller = Controller()
        self.createur = Creator()
#        controller.run()

    def main_menu(self):

        View.menu_format("Application d'échec",
                         "Menu principal",
                         type='title'
                         )
        # TODO : utiliser enumerate pour la numérotation ?
        View.menu_format("1 - Gestion joueurs",
                         "2 - Gestion Tournois",
                         type='choice'
                         )

        View.menu_input(self.menu_player, self.menu_tournament)

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
            for texte in args:
                print(texte)
            # print("Tapez le numéro de l'option souhaitée :")

    @staticmethod
    def menu_input(* args):
        choix = ""

        # ajoute par défaut l'option pour quitter a tous les menus
        num_quit = len(args) + 1
        View.menu_format(str(num_quit) + " - Quitter",
                         type='choice'
                         )

        # tant que l'on ne quitte pas...
        # TODO : trouver autre chose que le while True
        while True:  # choix != num_quit:
            try:
                choix = int(input("Choix : "))
    #                if isinstance(int(choix), int):
                if choix == num_quit:
                    break
                print(args[choix - 1])
                args[choix - 1]()
                break
            except ValueError:
                print("Merci de saisir un numéro.")
            except IndexError:
                print("Merci de saisir un numéro valide.")
            except Exception as e:
                print(e)

    @staticmethod
    def check_choice(self, choice):
        return isinstance(int(choice), int)

    def menu_player(self):
        View.menu_format("Menu joueurs", type='title')
        View.menu_format("1 - Création joueur",
                         "2 - Génération joueur (POUR TEST UNIQUEMENT)",
                         "3 - Retour au menu principal",
                         type='choice'
                         )
        View.menu_input(self.player_create, self.player_generate, self.main_menu)


    def menu_tournament(self):
        View.menu_format("Menu tournois", type='title')
        View.menu_format("1 - Nouveau tournoi",
                         "2 - Génération tournoi (POUR TEST UNIQUEMENT)",
                         "3 - Modifier Tournoi",
                         "4 - Menu principal",
                         type='choice'
                         )
        View.menu_input(self.tournament_create, self.tournament_generate, self.tournament_modify, self.main_menu)

    def player_create(self):
        View.menu_format("Création joueur", type='title')
        print("Saisir le nom de famille :")
        last_name = input()
        print("Saisir le prénom :")
        first_name = input()
        print("Saisir la date de naissance au format AAAA-MM-JJ :")
        birthdate = input()
        self.controller.manage_player.create(last_name=last_name, first_name=first_name, birthdate=birthdate)
        # on retourne sur le menu précédent
        self.menu_player()

    def player_generate(self):
        print("Saisir nombre de joueurs à créer")
        nb_players = int(input())
        self.createur.player(nb_players)
        print("Génération des joueurs : " + str(Player.get_player_repertory()))
        # on retourne sur le menu précédent
        self.menu_player()

    def tournament_create(self):
        View.menu_format("Création d'un tournoi", type='title')
        name = input("Nom du tournoi > ")
        location = input("lieu > ")
        start_date = input("date début (format AAA/MM/JJ) > ")
        end_date = input("date fin (format AAA/MM/JJ) > ")
        number_of_rounds = input("Nombre tours (4 par défaut) > ")
        description = input("Description > ")
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
        print("Saisir le nombre de tournois à générer")
        nb_tournaments = int(input())
        toto = self.createur.tournament(nb_tournaments)
        print("Génération des tournois : " + str(Tournament.get_tournament_repertory()))
        # on retourne sur le menu précédent
        self.menu_tournament()

    def tournament_modify(self):
        View.menu_format("Indiquer l'ID du tournoi à modifier", type='title')
        input("ID > ")
        pass
        self.menu_tournament()
