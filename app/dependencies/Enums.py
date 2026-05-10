from enum import StrEnum, auto


class Status(StrEnum):
    todo=auto()
    in_progress=auto()
    done=auto()

class Priority(StrEnum):
    high=auto()
    medium=auto()
    low=auto()