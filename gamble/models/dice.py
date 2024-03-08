"""
die and dice submodule
"""

import random
from gamble.errors import GambleException


class Die:
    """
    a single die object

    Args:
        sides: the number of sides to this die
    """

    def __init__(self, sides: int = 6) -> None:
        if abs(int(sides)) < 2:
            raise GambleException("A die must have at least 2 sides")
        self.sides = abs(int(sides))
        self.negative = sides <= 0
        self.multiplier = -1 if self.negative else 1
        self.rolls = 0

    def __str__(self) -> str:
        """
        dunder str method

        Returns:
            the string representation of this die
        """
        return f"<{'-' if self.negative else ''}d{self.sides} Die>"

    def __repr__(self) -> str:
        """
        dunder repr method

        Returns:
            the repr representation of this die
        """
        return self.__str__()

    def __lt__(self, other: "Die") -> bool:
        """
        dunder less than method

        Args:
            other: another Die instance

        Returns:
            true if this die is smaller than the other die
        """
        return self.net_sides < other.net_sides

    def __gt__(self, other: "Die") -> bool:
        """
        dunder greater than method

        Args:
            other: another Die instance

        Returns:
            true if this die is bigger than the other die
        """
        return self.net_sides > other.net_sides

    def __le__(self, other: "Die") -> bool:
        """
        dunder less than or equal to method

        Args:
            other: another Die instance

        Returns:
            true if this die is smaller than or equal to the other die
        """
        return self < other or self == other

    def __ge__(self, other: "Die") -> bool:
        """
        dunder greater than or equal to method

        Args:
            other: another Die instance

        Returns:
            true if this die is bigger than or equal to the other die
        """
        return self > other or self == other

    @property
    def net_sides(self) -> int:
        """
        the raw max sides * multiplier

        Returns:
            the non-absolute value of this die's sides
        """
        return self.sides * self.multiplier

    @property
    def max(self) -> int:
        """
        the max value this die can roll

        Returns:
            the max for this die
        """
        return -1 if self.negative else self.sides

    @property
    def min(self) -> int:
        """
        the min value this die can roll

        Returns:
            the min for this die
        """
        return self.sides if self.negative else 1

    def roll(self) -> int:
        """
        roll the die

        Returns:
            the value rolled by this die
        """
        value = random.randrange(self.sides) + 1  # nosec
        self.rolls += 1
        return value * self.multiplier


class RiggedDie(Die):
    """
    a die with a modifier to roll in the top 3 per the percentage passed in

    Args:
        sides: the number of sides to this die
        rigged_factor: int from 0-100 to manipulate the die into a high roll
    """

    def __init__(self, sides: int = 6, rigged_factor: int = 50) -> None:
        self.rigged_factor = rigged_factor
        if rigged_factor < 0 or rigged_factor > 100:
            raise GambleException("The rigged factor must be between 0 and 100")
        if sides < 2:
            raise GambleException("the die must have at least 2 sides")

        super().__init__(sides)

    def roll(self) -> int:
        """
        sometime override supers die roll depending on the rigged_factor

        Returns:
            the value rolled by this die
        """
        if random.randrange(101) <= self.rigged_factor:  # nosec
            value = [self.sides, self.sides - 1, self.sides - 2][random.randrange(3)]  # nosec
            self.rolls += 1
            return value * self.multiplier
        return super().roll()


class Dice:
    """
    a group of die objects

    Args:
        init_string: a d-notation string representing a set of dice
        rigged_factor: int from 0-100 to manipulate the die into a high roll
    """

    def __init__(self, init_string: str = "2d6", rigged_factor: int = -1) -> None:
        self.__d_string = init_string.strip().lower().replace("-", "+-")
        self.d_strings = [x.strip() for x in self.__d_string.split("+")]
        self.dice: list[Die | RiggedDie] = []
        self.bonuses: list[int] = []

        for d_string in self.d_strings:
            if "d" in d_string:
                die_settings = [int(x) for x in d_string.split("d") if x]
                if len(die_settings) == 1:
                    self.dice.append(self.create_die(die_settings[0], rigged_factor=rigged_factor))
                elif len(die_settings) > 1:
                    num, value = die_settings
                    negative = -1 if num < 0 else 1
                    self.dice.extend(
                        [self.create_die(value * negative, rigged_factor=rigged_factor)] * abs(num)
                    )
                else:
                    raise GambleException("cannot create a die with no value!")
            else:
                self.bonuses.append(int(d_string))
        self.dice = sorted(self.dice)
        self.bonuses = sorted(self.bonuses)
        self.rolls = 0

    def __str__(self) -> str:
        """
        dunder str method

        Returns:
            the string representation of this set of dice
        """
        dice_string = "\n".join([str(x) for x in self.parts])
        return f"{{\n{dice_string}\n}}"

    def __repr__(self) -> str:
        """
        dunder repr method

        Returns:
            the repr representation of this set of dice
        """
        return self.__str__()

    @property
    def parts(self) -> list[Die | int]:
        """
        listing of the parts of this roll + bonuses

        Returns:
            a list of the parts of this dice calculation
        """
        return [*self.dice, *self.bonuses]

    @property
    def max(self) -> int:
        """
        the max value these dice can roll

        Returns:
            the max for these dice + bonuses
        """
        return sum([*[x.max for x in self.dice], *self.bonuses])

    @property
    def min(self) -> int:
        """
        the min value these dice can roll

        Returns:
            the min for these dice + bonuses
        """
        return sum([*[x.min for x in self.dice], *self.bonuses])

    def create_die(self, sides: int, rigged_factor: int = -1) -> Die | RiggedDie:
        """
        helper to create dice

        Args:
            sides: the number of sides on a die
            rigged_factor: int from 0-100 to manipulate the die into a high roll

        Returns:
            A Die object that can be rigged
        """
        if rigged_factor != -1:
            return RiggedDie(sides, rigged_factor)
        return Die(sides)

    def roll(self) -> int:
        """
        roll the dice

        Returns:
            the value rolled by this dice
        """
        self.rolls += 1
        rolls = [x.roll() for x in self.dice]
        return sum([*rolls, *self.bonuses])

    def roll_many(self, num_rolls: int = 2) -> list[int]:
        """
        roll dice multiple times

        Args:
            num_rolls: the number of times to roll the dice

        Returns:
            list of values rolled by these dice
        """
        return [self.roll() for _ in range(num_rolls)]

    def max_of(self, num_rolls: int = 2) -> tuple[int, list[int]]:
        """
        roll dice multiple times

        Args:
            num_rolls: the number of times to roll the dice

        Returns:
            a tuple with the max value rolled by the dice, and the dice rolls
        """
        rolls = self.roll_many(num_rolls)
        max_roll = max(rolls)
        return max_roll, rolls

    def min_of(self, num_rolls: int = 2) -> tuple[int, list[int]]:
        """
        roll dice multiple times

        Args:
            num_rolls: the number of times to roll the dice

        Returns:
            a tuple with the min value rolled by the dice, and the dice rolls
        """
        rolls = self.roll_many(num_rolls)
        min_roll = min(rolls)
        return min_roll, rolls
