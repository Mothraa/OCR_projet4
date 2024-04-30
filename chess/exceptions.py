class TournamentAlreadyAddedError(Exception):
    """Exception raised when a tournament is already added to the player's history"""
    tournament_name = None

    def __init__(self, tournament_name):
        self.tournament_name = tournament_name
        super().__init__(f"Le tournoi '{tournament_name}' a déjà été ajouté à l'historique.")


class InvalidDateFormatError(Exception):
    """Exception raised when the date format is invalid"""
    pass
