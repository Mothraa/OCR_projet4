from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

# class MainOption(ExtendedEnum):
#     PLAYER_MENU_OPTION = 1
#     TOURNAMENT_MENU_OPTION = 2
#     CLOSE_PROGRAM_OPTION = 3


class TournamentStatus(ExtendedEnum):
    CREATED = 1
    IN_PROGRESS = 2
    TERMINATED = 3