"""
tests for the dice submodule of gamble
"""
import pytest
from gamble import Die, RiggedDie, Dice
from gamble.errors import GambleException


def test_die_init() -> None:
    """tests the use of a single die"""
    die = Die()
    assert die.sides == 6
    assert die.max == 6
    assert die.min == 1
    assert die.rolls == 0
    assert die.net_sides == die.sides
    assert str(die) == "<d6 Die>"
    assert repr(die) == "<d6 Die>"
    assert not die > die
    assert not die < die
    assert die >= die
    assert die <= die


def test_rigged_die_init() -> None:
    """tests the use of a single rigged die"""
    die = RiggedDie(6, 100)
    assert die.sides == 6
    assert die.max == 6
    assert die.min == 1
    assert die.rolls == 0
    assert die.net_sides == die.sides
    assert die.rigged_factor == 100
    assert str(die) == "<d6 Die>"
    assert repr(die) == "<d6 Die>"
    assert not die > die
    assert not die < die
    assert die >= die
    assert die <= die


def test_dice_init() -> None:
    """tests creating a set of dice"""
    dice = Dice()
    assert dice.rolls == 0
    assert not dice.bonuses
    assert dice.max == 12
    assert dice.min == 2
    assert dice.parts
    assert str(dice) == "{\n<d6 Die>\n<d6 Die>\n}"
    assert repr(dice) == "{\n<d6 Die>\n<d6 Die>\n}"

    roll = dice.roll()
    assert 2 <= roll <= 12
    assert dice.rolls == 1

    # test that you can't make just a 'd'
    try:
        dice = Dice("d")
        assert False
    except GambleException:
        assert True


def test_dice_complex() -> None:
    """tests complex dice string setup"""
    dice = Dice("d20+8", 100)
    assert dice.rolls == 0
    assert dice.bonuses
    assert dice.max == 28
    assert dice.min == 9
    assert dice.parts
    assert all(
        [die.rigged_factor == 100 for die in dice.dice if isinstance(die, RiggedDie)]
    )


def test_broken_die() -> None:
    """tests broken issues with the die class"""
    with pytest.raises(Exception):
        Die(sides=1)

    with pytest.raises(Exception):
        RiggedDie(6, 1000)

    with pytest.raises(Exception):
        RiggedDie(6, -1)


def test_dice_rolls() -> None:
    """tests multiple rolls of dice"""
    dice = Dice("d20")
    assert dice.rolls == 0

    rolls = dice.roll_many(2)
    assert dice.rolls == 2
    assert len(rolls) == 2
    assert 1 <= rolls[0] <= 20
    assert 1 <= rolls[1] <= 20


def test_dice_max_of() -> None:
    """tests rolling the max of x dice"""
    dice = Dice("d20")
    assert dice.rolls == 0
    assert not dice.bonuses

    the_roll, rolls = dice.max_of(3)
    assert dice.rolls == 3
    assert len(rolls) == 3
    assert 1 <= rolls[0] <= 20
    assert 1 <= rolls[1] <= 20
    assert 1 <= rolls[2] <= 20
    assert the_roll == max(rolls)


def test_dice_min_of() -> None:
    """tests rolling the min of x dice"""
    dice = Dice("d20")
    assert dice.rolls == 0
    assert not dice.bonuses

    the_roll, rolls = dice.min_of(4)
    assert dice.rolls == 4
    assert len(rolls) == 4
    assert 1 <= rolls[0] <= 20
    assert 1 <= rolls[1] <= 20
    assert 1 <= rolls[2] <= 20
    assert 1 <= rolls[3] <= 20
    assert the_roll == min(rolls)


def test_roll_rigged_die() -> None:
    """tests the use of a single rigged die"""
    dice = Dice("d20", 100)

    the_roll, rolls = dice.min_of(100)
    assert min(rolls) == 18

    the_roll, rolls = dice.max_of(100)
    assert max(rolls) == 20
