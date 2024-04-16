from operator import itemgetter

from chess.utils import TournamentStatus


class Tournament:

    id = None
    name = None
    location = None
    status = None
    start_date = None
    end_date = None
    description = None
    number_of_rounds = None
    current_round_number = None
    rounds_list = []
    player_list = []
    tournaments_repertory = []

    def __init__(self,  tournament_data):
        # condition pour gérer le cas de l'import JSON ou l'on ne régénère pas les ID :
        if tournament_data.id is None:
            self.id = self.__create_id()
        else:
            self.id = tournament_data.id
        self.id = self.__create_id()
        self.name = tournament_data.name
        self.location = tournament_data.location
        self.status = TournamentStatus.CREATED
        self.start_date = tournament_data.start_date
        self.end_date = tournament_data.end_date
        self.description = tournament_data.description
        self.number_of_rounds = tournament_data.number_of_rounds
        self.current_round_number = 0
        self.rounds_list = tournament_data.rounds_list
        self.player_list = tournament_data.player_list

        Tournament.tournaments_repertory.append(self)

    def __create_id(self):
        _id = len(Tournament.tournaments_repertory)
        return _id

    def get_status(self) -> TournamentStatus:
        return self.status

    def get_player_list(self):
        return self.player_list

    def set_player_list(self, new_player_list):
        self.player_list = new_player_list

    def get_current_round_number(self):
        return self.current_round_number

    def get_current_round(self):
        round_indice = self.get_current_round_number() - 1
        chess_round = self.rounds_list[round_indice]
        return chess_round

    def add_player_to_tournament(self, player):
        INIT_SCORE = 0.0
        # TODO : on enregistre que l'id du joueur pour régler un pb de serialisation json
        self.player_list.append((player.id, INIT_SCORE))

    def change_status(self, new_status: TournamentStatus):
        actual_status = self.get_status()
        if actual_status == TournamentStatus.TERMINATED:
            raise PermissionError("on ne peut modifier le statut d'un tournoi terminé")
        elif actual_status == TournamentStatus.IN_PROGRESS and new_status == TournamentStatus.CREATED:
            raise PermissionError("on ne peut repasser CREATED, un tournoi IN PROGRESS")
        else:
            self.status = new_status

    def add_score_in_tournament_ranking(self, score_to_add: float, player_id):
        player_list = self.get_player_list()
        player_index = None
        for index, (p_id, _) in enumerate(player_list):
            if p_id == player_id:
                player_index = index
                break
        (_, score) = player_list[player_index]
        new_score = score + score_to_add
        self.player_list[player_index] = (player_id, new_score)

        # TODO : déplacer le set_player_list dans le controller une fois tous les scores modifiés pour limiter les maj
        self.set_player_list(player_list)

    def sort_players_by_score(self):
        # la liste des joueurs contient des éléments de la forme (Player, score)
        self.player_list.sort(key=itemgetter(1), reverse=True)

    @staticmethod
    def get_tournaments_repertory():
        return Tournament.tournaments_repertory

    @staticmethod
    def find_by_id(tournament_id: int):
        return Tournament.tournaments_repertory[tournament_id]

    def __repr__(self) -> str:
        return "ID {} : {} - Du {} au {} - {} tours".format(self.id,
                                                            self.name,
                                                            self.start_date,
                                                            self.end_date,
                                                            self.number_of_rounds,
                                                            )

    # Méthode pour sérialiser l'objet en un dictionnaire
    def encode(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description,
            "rounds_list": [round.__dict__() for round in self.rounds_list]  # Serialisation d'objets imbriqués
        }


class Round:
    def __init__(self, **kwargs):
        self.id = kwargs.get("round_number")
        self.round_name = f"Tour {kwargs.get("round_number")}"
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")
        self.matchs_list = []

    def add_match(self):
        """ format des matchs :
        ([player1, score_player1], [player2, score_player2])
        """
        # TODO
        pass

    def get_matchs_list(self):
        return self.matchs_list

    # pour la sérialisation
    # def __dict__(self):
    #     return {
    #         "id": self.id,
    #         "round_name": self.round_name,
    #         "start_date": self.start_date,
    #         "end_date": self.end_date,
    #         "matchs_list": [match.__dict__() for match in self.matchs_list]
        # }

class Player:
    id = None
    national_chess_id = None
    first_name = None
    last_name = None
    birthdate = None
    tournaments_history = []
    matchs_history = []
    players_repertory = []

    def __init__(self, player_data: dict):
        # condition pour gérer le cas de l'import JSON ou l'on ne régénère pas les ID :
        if player_data.get('id') is None:
            self.id = self.__create_id()
        else:
            self.id = player_data['id']
        self.national_chess_id = player_data.get('national_chess_id')
        self.first_name = player_data.get('first_name')
        self.last_name = player_data.get('last_name')
        self.birthdate = player_data.get('birthdate')
        self.tournaments_history = player_data.get('tournaments_history')
        self.matchs_history = player_data.get('matchs_history')
        Player.players_repertory.append(self)

    def __create_id(self):
        id = len(Player.players_repertory)
        return id

    @staticmethod
    def get_players_repertory():
        """Liste de tous les joueurs"""
        return Player.players_repertory

    @staticmethod
    def find_by_id(player_id: int):
        """Retourne un jouer depuis son ID"""
        return Player.players_repertory[player_id]

    # TODO : je ne peux pas déclarer def add_tournament_from(self, tournament: Tournament)
    # car Tournament pas encore def... comment faire ?
    def add_tournament(self, tournament):
        # TODO : on ajoute l'ID de tournament plutot que le tournoi pour régler le pb de serialisation
        self.tournaments_history.append(tournament.id)

    # def add_tournament_by_id(self, tournament_id: int):
    #     self.add_tournament(Tournament.find_by_id(tournament_id))

    def get_tournament_history(self):
        """Historique des tournois joués"""
        return self.tournaments_history

    def set_matchs_history(self, tournament, round, match):
        # match sous la forme : ([player1, score1], [player2, score2])
        # TODO a déplacer dans service
        (player1, score1), (player2, score2) = match

        # on détermine si le joueur est indiqué par player1 ou player2
        adversaire = player2 if player1 is self else player1
        score_joueur = score1 if player1 is self else score2
        score_adversaire = score2 if player1 is self else score1

        # format : liste de tuples => (ID tournoi, round, ID adversaire, score_joueur, score_adversaire)
        self.matchs_history.append((tournament.id, round.id, adversaire.id, score_joueur, score_adversaire))

    def get_matchs_history(self):
        """ Historique des matchs joués :
            format, liste de tuples => (ID tournoi, round, ID adversaire, score_joueur, score_adversaire)
        """
        list_history = []
        return list_history

    def get_matchs_history_by_tournament(self, tournament):
        """ Historique des matchs joués par tournoi :
            format, liste de tuples => (ID tournoi, round, ID adversaire, score_joueur, score_adversaire)
        """
        full_list = self.get_matchs_history()
        list_history = [x for x in full_list if x[0] == tournament.id]
        return list_history

    def __repr__(self) -> str:
        return "ID {}: {} {}".format(self.id,
                                     self.first_name,
                                     self.last_name,
                                     )

    def encode(self):
        return self.__dict__
