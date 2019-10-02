"""
@author jacobi petrucciani
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
    """
    @desc a golf hole object
    """

    def __init__(self, tee: int, yards: int, par: int, handicap: int) -> None:
        """
        @cc 1
        @desc hole constructor
        @arg tee: the tee number for this hole
        @arg yards: the number of yards from tee to hole
        @arg par: the par for this hole
        @arg handicap: the handicap value for this hole
        """
        self.tee = tee
        self.yards = yards
        self.par = par
        self.handicap = handicap


class Course:
    """
    @desc a golf course object
    """

    def __init__(self, name: str, holes: List[Hole]) -> None:
        """
        @cc 1
        @desc course constructor
        @arg name: the name of this golf course
        @arg holes: a list of holes in this golf course
        """
        self.name = name
        self.holes = sorted(holes, key=lambda hole: hole.tee)
        self.yards = sum(x.yards for x in self.holes)
        self.par = sum(x.par for x in self.holes)
        self.front = self.holes[:9]
        self.back = self.holes[9:]


class Player:
    """
    @desc a golf player object
    """

    def __init__(self, name: str, handicap: int) -> None:
        """
        @cc 1
        @desc player constructor
        @arg name: the name of the player
        @arg handicap: the handicap of the player
        """
        self.name = name
        self.handicap = handicap


class Group:
    """
    @desc a golf group object
    """

    def __init__(self, course: Course, players: List[Player]) -> None:
        """
        @cc 1
        @desc group constructor
        @arg course: the course that this group is playing
        @arg players: the list of players in this group
        """
        self.course = course
        self.players = players
        self.scores = []  # type: ignore


HOLES = [Hole(index + 1, x[0], x[1], x[2]) for index, x in enumerate(HCC_DATA)]
HCC = Course("Hillcrest", HOLES)
