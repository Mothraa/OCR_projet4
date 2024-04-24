



from chess.service import GeneratePlayerService, GenerateTournamentService
from chess.controller import PlayerController, TournamentController


# timezone = ZoneInfo("Europe/Paris")



class JsonTest():

    def run():

        # a voir si utile à garder, on converti les dates en amont
        # def datetime_handler(obj):
        #     if isinstance(obj, (datetime, date)):
        #         return obj.isoformat()
        # #        return str(obj.strftime("%Y-%m-%d %H:%M:%S"))eee

        # json.JSONEncoder.default = datetime_handler

        # player_service = GeneratePlayerService()
        # player_controller = PlayerController()
        # tournament_controller = TournamentController()
        # tournmament_service = GenerateTournamentService()
        # json_instance = JsonManagement()

        # command_player = player_service.generate_player_all_attrs()
        # joueur = player_controller.player_create(command_player)
        # # print(type(joueur_convert))
        # # print(joueur_convert)
        # json_instance.save_player_as_json(joueur)

        # command_tournament = tournmament_service.generate_tournament_all_attrs()
        # tournoi = tournament_controller.tournament_create(command_tournament)

        # json_instance.save_tournament_as_json(tournoi)
        # # Enregistrer l'objet principal dans un fichier JSON
        # chemin_fichier_json_principal = "joueur_principal.json"
        # with open(chemin_fichier_json_principal, "w") as fichier_json_principal:
        #     json.dump(objet_dict, fichier_json_principal, indent=4)

        # # Enregistrer players_repertory dans un autre fichier JSON
        # chemin_fichier_json_repertory = "players_repertory.json"
        # players_repertory = joueur.players_repertory
        # with open(chemin_fichier_json_repertory, "w") as fichier_json_repertory:
        #     json.dump(players_repertory, fichier_json_repertory, indent=4)
