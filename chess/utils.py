from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class TournamentStatus(ExtendedEnum):
    CREATED = 1
    IN_PROGRESS = 2
    TERMINATED = 3
