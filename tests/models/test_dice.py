"""
tests for the dice submodule of gamble
"""
import gamble


def test_die():
    """tests the use of a single die"""
    die = gamble.Die()
    assert die.sides == 6
    assert die.max == 6
    assert die.min == 1
    assert die.rolls == 0
    assert die.net_sides == die.sides
