"""
tests for the cards submodule of gamble
"""
import pytest
import random
from gamble import Card, Deck, EuchreDeck, Hand
from gamble.errors import InvalidCard


random.seed(420)


def test_card_init() -> None:
    """test that a card can be created"""
    card = Card()
    assert card.suit == Card.Suits.SPADES
    assert card.full_name == "ace of spades"
    assert str(card) == "A♠"
    assert repr(card) == "<Card:A♠>"
    assert card.unicode == "🂡"
    assert card.color == Card.BLACK
    assert card == card
    assert card != "test"
    assert not card < card
    assert not card > card
    assert card <= card
    assert card >= card
    assert card.is_black
    assert not card.is_red

    with pytest.raises(InvalidCard):
        Card.get("XXX")

    with pytest.raises(InvalidCard):
        Card.get("ZS")

    with pytest.raises(InvalidCard):
        Card.get("AZ")

    # check that the unicode lookup works
    seven = Card(value=Card.Values.SEVEN, suit=Card.Suits.DIAMONDS)
    assert seven
    assert seven.unicode == "🃇"


def test_deck_init() -> None:
    """test that we can create a deck of cards"""
    deck = Deck(shuffle=False)
    top = deck.top
    bottom = deck.bottom
    assert len(deck.cards) == 52
    assert deck.cards_left == 52
    assert top.value.name == "ace"
    assert top.suit.name == "spades"
    assert top.unicode == "🂡"
    assert bottom.value.name == "king"
    assert bottom.suit.name == "hearts"
    assert bottom.unicode == "🂾"
    assert top in deck
    assert "test" not in deck

    draw = deck.draw()
    assert draw not in deck
    assert isinstance(draw, Card)
    assert deck.top.unicode == "🂢"
    assert draw.value.name == "ace"
    assert draw.suit.name == "spades"

    draw_multiple = deck.draw(times=5)
    assert isinstance(draw_multiple, list)
    assert str(deck) == "<Deck[46]>"
    assert repr(deck) == "<Deck[46]>"

    last_top = deck.top
    deck.shuffle(times=10)
    assert last_top != deck.top


def test_euchre_deck() -> None:
    """tests a euchre specific deck"""
    deck = EuchreDeck(shuffle=False)
    assert deck.cards_left == 24


def test_hands() -> None:
    """test that we can interact with hands"""
    deck = Deck(shuffle=False)
    hand = deck.draw_hand()
    assert len(hand) == 5
    assert str(hand) == "[A♠, 2♠, 3♠, 4♠, 5♠]"
    assert repr(hand) == "<Hand[5](straight flush) [A♠, 2♠, 3♠, 4♠, 5♠]>"


def test_hand_ranks() -> None:
    """test all the supported hand ranks"""
    high_card = Hand.get("2c,3c,4c,5c,Kh")
    assert high_card.rank == Hand.Ranks.HIGH_CARD

    one_pair = Hand.get("2c,3c,4c,Kc,Kh")
    assert one_pair.rank == Hand.Ranks.PAIR

    two_pair = Hand.get("2c,4h,4c,Kc,Kh")
    assert two_pair.rank == Hand.Ranks.TWO_PAIR

    three_of_a_kind = Hand.get("2c,4h,Ks,Kc,Kh")
    assert three_of_a_kind.rank == Hand.Ranks.THREE_OF_A_KIND

    low_straight = Hand.get("2c,3h,4c,5c,Ah")
    assert low_straight.rank == Hand.Ranks.STRAIGHT

    high_straight = Hand.get("Tc,Jh,Qc,Kc,Ah")
    assert high_straight.rank == Hand.Ranks.STRAIGHT

    flush = Hand.get("2c,3c,4c,5c,Kc")
    assert flush.rank == Hand.Ranks.FLUSH

    full_house = Hand.get("2c,2s,2h,Ks,Kc")
    assert full_house.rank == Hand.Ranks.FULL_HOUSE

    four_of_a_kind = Hand.get("2c,2s,2h,2d,Kc")
    assert four_of_a_kind.rank == Hand.Ranks.FOUR_OF_A_KIND

    low_straight_flush = Hand.get("As,2s,3s,4s,5s")
    assert low_straight_flush.rank == Hand.Ranks.STRAIGHT_FLUSH
    assert low_straight_flush.is_straight_flush

    high_straight_flush = Hand.get("As,Ts,Js,Qs,Ks")
    # assert high_straight_flush.rank == Hand.Ranks.STRAIGHT_FLUSH
    assert high_straight_flush.rank == Hand.Ranks.ROYAL_FLUSH
    assert high_straight_flush.is_royal_flush

    assert two_pair > one_pair
    assert low_straight_flush < high_straight_flush
