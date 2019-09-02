"""
dice submodule
"""
import random
from typing import List, Union


class Die:
    """a single die object"""

    def __init__(self, sides: int = 6) -> None:
        """create a new die"""
        if abs(int(sides)) < 2:
            raise Exception("A die must have at least 2 sides")
        self.sides = abs(int(sides))
        self.negative = sides <= 0
        self.multiplier = -1 if self.negative else 1
        self.rolls = 0

    def __str__(self) -> str:
        """string representation"""
        return "<{}d{} Die>".format("-" if self.negative else "", self.sides)

    def __repr__(self) -> str:
        """repr"""
        return self.__str__()

    def __lt__(self, other: "Die") -> bool:
        """less than dunder method"""
        return self.net_sides < other.net_sides

    def __gt__(self, other: "Die") -> bool:
        """greater than dunder method"""
        return self.net_sides > other.net_sides

    def __le__(self, other: "Die") -> bool:
        """less than or equal to dunder method"""
        return self < other or self == other

    def __ge__(self, other: "Die") -> bool:
        """greater than or equal to dunder method"""
        return self > other or self == other

    @property
    def net_sides(self) -> int:
        """the raw max sides * multiplier"""
        return self.sides * self.multiplier

    @property
    def max(self) -> int:
        """returns the max value this die can roll"""
        return -1 if self.negative else self.sides

    @property
    def min(self) -> int:
        """returns the min value this die can roll"""
        return self.sides if self.negative else 1

    def roll(self) -> int:
        """roll the die"""
        value = random.randrange(self.sides) + 1
        self.rolls += 1
        return value * self.multiplier


class Dice:
    """a group of die objects"""

    def __init__(self, init_string: str = "2d6") -> None:
        """create a new d notation group of dice"""
        self.__d_string = init_string.strip().lower().replace("-", "+-")
        self.d_strings = [x.strip() for x in self.__d_string.split("+")]
        self.dice: List[Die] = []
        self.bonuses: List[int] = []
        for d_string in self.d_strings:
            if "d" in d_string:
                die_settings = [int(x) for x in d_string.split("d") if x]
                if len(die_settings) == 1:
                    self.dice.append(Die(die_settings[0]))
                elif len(die_settings) > 1:
                    num, value = die_settings
                    negative = -1 if num < 0 else 1
                    self.dice.extend([Die(value * negative)] * abs(num))
            else:
                self.bonuses.append(int(d_string))
        self.dice = list(sorted(self.dice))
        self.bonuses = list(sorted(self.bonuses))
        self.rolls = 0

    def __str__(self) -> str:
        """string representation of the dice"""
        return "{{\n{}\n}}".format("\n".join([str(x) for x in self.parts]))

    def __repr__(self) -> str:
        """repr"""
        return self.__str__()

    @property
    def parts(self) -> List[Union[Die, int]]:
        """returns the listing of the parts of this roll + bonuses"""
        return [*self.dice, *self.bonuses]

    @property
    def max(self) -> int:
        """returns the max value these dice + bonuses could return"""
        return sum([*[x.max for x in self.dice], *self.bonuses])

    @property
    def min(self) -> int:
        """returns the min value these dice + bonuses could return"""
        return sum([*[x.min for x in self.dice], *self.bonuses])

    def roll(self, verbose: bool = False) -> int:
        """rolls the group of dice"""
        self.rolls += 1
        rolls = [x.roll() for x in self.dice]
        return sum([*rolls, *self.bonuses])
