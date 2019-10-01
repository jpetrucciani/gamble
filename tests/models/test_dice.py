"""
tests for the dice submodule of gamble
"""
import pytest
from gamble import Die, Dice


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


def test_dice_complex() -> None:
    """tests complex dice string setup"""
    dice = Dice("d20+8")
    assert dice.rolls == 0
    assert dice.bonuses
    assert dice.max == 28
    assert dice.min == 9
    assert dice.parts

def test_broken_die() -> None:
    """tests broken issues with the die class"""
    with pytest.raises(Exception):
        Die(sides=1)

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
