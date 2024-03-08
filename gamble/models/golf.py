"""
golf related games
"""

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
HCC_DATA = zip(YARDS, PAR, HANDICAP, strict=True)


class Hole:
    """
    a golf hole object
    """

    def __init__(self, tee: int, yards: int, par: int, handicap: int) -> None:
        """
        hole constructor

        Args:
            tee: the tee number for this hole
            yards: the number of yards from tee to hole
            par: the par for this hole
            handicap: the handicap value for this hole
        """
        self.tee = tee
        self.yards = yards
        self.par = par
        self.handicap = handicap


class Course:
    """
    a golf course object

    Args:
        name: the name of this golf course
        holes: a list of holes in this golf course
    """

    def __init__(self, name: str, holes: list[Hole]) -> None:
        self.name = name
        self.holes = sorted(holes, key=lambda hole: hole.tee)
        self.yards = sum(x.yards for x in self.holes)
        self.par = sum(x.par for x in self.holes)
        self.front = self.holes[:9]
        self.back = self.holes[9:]


class Player:
    """
    a golf player object

    Args:
        name: the name of the player
        handicap: the handicap of the player
    """

    def __init__(self, name: str, handicap: int) -> None:
        self.name = name
        self.handicap = handicap


class Group:
    """
    a golf group object

    Args:
        course: the course that this group is playing
        players: the list of players in this group
    """

    def __init__(self, course: Course, players: list[Player]) -> None:
        self.course = course
        self.players = players
        self.scores = []  # type: ignore


HOLES = [Hole(index + 1, x[0], x[1], x[2]) for index, x in enumerate(HCC_DATA)]
HCC = Course("Hillcrest", HOLES)
