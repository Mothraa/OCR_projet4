
from chess.controller import Controller

class View:


    def __init__(self):
        # controller = Controller()
        # controller.run()
        pass

    def main_menu(self):

        View.menu_format("Application d'échec",
                         "Menu principal",
                         type='title'
                         )
        View.menu_format("1 - Gestion joueurs",
                         "2 - Gestion Tournois",
                         type='choice'
                         )

        View.menu_input(self.menu_player, self.menu_tournament)

    @staticmethod
    def menu_format(*args, type):

        if type == "title":

            max_len = 0
            for texte in args:
                if max_len < len(texte):
                    max_len = len(texte)
            max_len = max_len + 10

            print("*" * max_len)
            print("*" + " " * (max_len-2) + "*")
            for texte in args:
                espace = int(round((max_len - len(texte)-2)/2, 0))
                texte_temp = "*" + " " * espace + texte + " " * espace + "*"
                print(texte_temp)
            print("*" + " " * (max_len-2) + "*")
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
                choix = int(input())
    #                if isinstance(int(choix), int):
                if choix == num_quit:
                    break
                print(args[choix - 1])
                print(type(args[choix - 1]))
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
                         "2 - Retour au menu principal",
                         type='choice'
                         )
        View.menu_input(self.menu_player_create, self.main_menu)


    def menu_tournament(self):
        View.menu_format("Menu tournois", type='title')
        View.menu_format("1 - Nouveau tournoi",
                         "2 - Modifier Tournoi",
                         "3 - Menu principal",
                         type='choice'
                         )

    def menu_player_create(self):
        pass
