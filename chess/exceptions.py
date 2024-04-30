class TournamentAlreadyAddedError(Exception):
    """Exception raised when a tournament is already added to the player's history"""
    tournament_name = None

    def __init__(self, tournament_name):
        self.tournament_name = tournament_name
        super().__init__(f"Le tournoi '{tournament_name}' a déjà été ajouté à l'historique.")


class NationalChessIdFormatError(ValueError):
    """Exception raised for invalid national chess ID format"""
    def __init__(self, message="Merci d'indiquer un identifiant national d'échec au bon format"):
        self.message = message
        super().__init__(self.message)


class InvalidDateFormatError(Exception):
    """Exception raised for invalid date format"""
    def __init__(self, message="Le format de date est invalide. Utilisez le format AAAA-MM-JJ."):
        self.message = message
        super().__init__(self.message)


class TournamentStatusError(Exception):
    """Exception raised for errors with the status of tournament"""
    def __init__(self, current_status):
        self.current_status = current_status
        super().__init__(f"Impossible d'effectuer l'action, le statut du tournoi est {self.current_status}")
