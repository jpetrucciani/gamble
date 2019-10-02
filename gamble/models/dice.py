"""
@author jacobi petrucciani
@desc die and dice submodule
"""
import random
from typing import List, Union, Tuple


class Die:
    """
    @desc a single die object
    """

    def __init__(self, sides: int = 6) -> None:
        """
        @cc 2
        @desc create a new die
        @arg sides: the number of sides to this die
        """
        if abs(int(sides)) < 2:
            raise Exception("A die must have at least 2 sides")
        self.sides = abs(int(sides))
        self.negative = sides <= 0
        self.multiplier = -1 if self.negative else 1
        self.rolls = 0

    def __str__(self) -> str:
        """
        @cc 1
        @desc dunder str method
        @ret the string representation of this die
        """
        return "<{}d{} Die>".format("-" if self.negative else "", self.sides)

    def __repr__(self) -> str:
        """
        @cc 1
        @desc dunder repr method
        @ret the repr representation of this die
        """
        return self.__str__()

    def __lt__(self, other: "Die") -> bool:
        """
        @cc 1
        @desc dunder less than method
        @arg other: another Die instance
        @ret true if this die is smaller than the other die
        """
        return self.net_sides < other.net_sides

    def __gt__(self, other: "Die") -> bool:
        """
        @cc 1
        @desc dunder greater than method
        @arg other: another Die instance
        @ret true if this die is bigger than the other die
        """
        return self.net_sides > other.net_sides

    def __le__(self, other: "Die") -> bool:
        """
        @cc 1
        @desc dunder less than or equal to method
        @arg other: another Die instance
        @ret true if this die is smaller than or equal to the other die
        """
        return self < other or self == other

    def __ge__(self, other: "Die") -> bool:
        """
        @cc 1
        @desc dunder greater than or equal to method
        @arg other: another Die instance
        @ret true if this die is bigger than or equal to the other die
        """
        return self > other or self == other

    @property
    def net_sides(self) -> int:
        """
        @cc 1
        @desc the raw max sides * multiplier
        @ret the non-absolute value of this die's sides
        """
        return self.sides * self.multiplier

    @property
    def max(self) -> int:
        """
        @cc 1
        @desc the max value this die can roll
        @ret the max for this die
        """
        return -1 if self.negative else self.sides

    @property
    def min(self) -> int:
        """
        @cc 1
        @desc the min value this die can roll
        @ret the min for this die
        """
        return self.sides if self.negative else 1

    def roll(self) -> int:
        """
        @cc 1
        @desc roll the die
        @ret the value rolled by this die
        """
        value = random.randrange(self.sides) + 1
        self.rolls += 1
        return value * self.multiplier


class Dice:
    """
    @desc a group of die objects
    """

    def __init__(self, init_string: str = "2d6") -> None:
        """
        @cc 2
        @desc create a new d notation group of dice
        @arg init_string: a d-notation string representing a set of dice
        """
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
        """
        @cc 1
        @desc dunder str method
        @ret the string representation of this set of dice
        """
        return "{{\n{}\n}}".format("\n".join([str(x) for x in self.parts]))

    def __repr__(self) -> str:
        """
        @cc 1
        @desc dunder repr method
        @ret the repr representation of this set of dice
        """
        return self.__str__()

    @property
    def parts(self) -> List[Union[Die, int]]:
        """
        @cc 1
        @desc listing of the parts of this roll + bonuses
        @ret a list of the parts of this dice calculation
        """
        return [*self.dice, *self.bonuses]

    @property
    def max(self) -> int:
        """
        @cc 1
        @desc the max value these dice can roll
        @ret the max for these dice + bonuses
        """
        return sum([*[x.max for x in self.dice], *self.bonuses])

    @property
    def min(self) -> int:
        """
        @cc 1
        @desc the min value these dice can roll
        @ret the min for these dice + bonuses
        """
        return sum([*[x.min for x in self.dice], *self.bonuses])

    def roll(self) -> int:
        """
        @cc 1
        @desc roll the dice
        @ret the value rolled by this dice
        """
        self.rolls += 1
        rolls = [x.roll() for x in self.dice]
        return sum([*rolls, *self.bonuses])

    def roll_many(self, num_rolls: int = 2) -> List[int]:
        """
        @cc 1
        @desc roll dice multiple times
        @arg num_rolls: the number of times to roll the dice
        @ret list of values rolled by these dice
        """
        rolls = [self.roll() for _ in range(0, num_rolls)]
        return rolls

    def max_of(self, num_rolls: int = 2) -> Tuple[int, List[int]]:
        """
        @cc 1
        @desc roll dice multiple times
        @arg num_rolls: the number of times to roll the dice
        @ret a tuple with the max value rolled by the dice, and the dice rolls
        """
        rolls = self.roll_many(num_rolls)
        max_roll = max(rolls)
        return max_roll, rolls
