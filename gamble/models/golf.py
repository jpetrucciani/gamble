"""
@desc golf related games
"""
from typing import List


YARDS = (
    332,
    410,
    357,
    148,
    431,
    519,
    338,
    405,
    283,
    515,
    348,
    148,
    446,
    348,
    380,
    431,
    217,
    389,
)
PAR = (4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 4, 3, 4, 4, 4, 4, 3, 4)
HANDICAP = (15, 3, 5, 17, 1, 9, 11, 7, 13, 6, 16, 18, 2, 14, 8, 4, 12, 10)
HCC_DATA = zip(YARDS, PAR, HANDICAP)


class Hole:
    """"""

    def __init__(self, tee: int, yards: int, par: int, handicap: int) -> None:
        """"""
        self.tee = tee
        self.yards = yards
        self.par = par
        self.handicap = handicap


class Course:
    """"""

    def __init__(self, name: str, holes: List[Hole]) -> None:
        """"""
        self.name = name
        self.holes = holes
        self.yards = sum(x.yards for x in self.holes)
        self.par = sum(x.par for x in self.holes)
        self.front = self.holes[:9]
        self.back = self.holes[9:]


class Player:
    """"""

    def __init__(self, name: str, handicap: int) -> None:
        """"""
        self.name = name
        self.handicap = handicap


class Group:
    """"""

    def __init__(self, course: Course, players: List[Player]) -> None:
        """"""


HOLES = [Hole(index + 1, x[0], x[1], x[2]) for index, x in enumerate(HCC_DATA)]
HCC = Course("Hillcrest", HOLES)
