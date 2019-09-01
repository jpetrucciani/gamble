"""
tests for the cards submodule of gamble
"""
from gamble import Card, Deck, EuchreDeck


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
    assert card.is_black
    assert not card.is_red

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
