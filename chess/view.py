

class View:


    def __init__(self):
        pass


    def MainMenu(self):

        View.separator("Application d'échec", "Menu principal", type='title')
        View.separator("1 - Gestion joueurs", "2 - Gestion Tournois", "3 - Quitter", type='choice')

        choix = ""

        while choix != "3":
            choix = input()
            if choix == "1":
                self.menu_player_create()
            elif choix == "2":
                self.menu_tournament_create()



#        modify_tournament()

        pass

    @staticmethod
    def separator(*args, type):

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
            print("Tapez le numéro de l'option souhaitée :")

    @staticmethod
    def check_choice(self, choice):
        return isinstance(int(choice), int)


    def menu_player_create(self):
        View.separator("Menu création de joueur", type='title')


    def menu_tournament_create(self):
        View.separator("Menu création de tournoi", type='title')
        View.separator("1 - Nouveau tournoi", "2 - Modifier Tournoi", "3 - Menu principal", "4 - Quitter", type='choice')

