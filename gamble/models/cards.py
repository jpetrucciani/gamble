"""
standard deck of cards submodule
"""
import random
from types import SimpleNamespace
from typing import Any, List, Union


class Suit(SimpleNamespace):
    """suit namespace class"""


class Value(SimpleNamespace):
    """value namespace class"""


class Card:
    """playing card model"""

    BLACK = 0
    RED = 1

    class Suits:
        """card suit enum"""

        SPADES = Suit(name="spades", char="♠", value=0, color=0, unicode=127136)
        CLUBS = Suit(name="clubs", char="♣", value=1, color=0, unicode=127184)
        DIAMONDS = Suit(name="diamonds", char="♦", value=2, color=1, unicode=127168)
        HEARTS = Suit(name="hearts", char="♥", value=3, color=1, unicode=127152)

        @classmethod
        def all(cls) -> List[Suit]:
            """get all suits"""
            return sorted(
                [
                    cls.__dict__[x]
                    for x in dir(cls)
                    if not x.startswith("_") and isinstance(cls.__dict__[x], Suit)
                ],
                key=lambda x: x.value,
            )

    class Values:
        """card value enum"""

        ACE = Value(char="A", name="ace", value=1)
        TWO = Value(char="2", name="two", value=2)
        THREE = Value(char="3", name="three", value=3)
        FOUR = Value(char="4", name="four", value=4)
        FIVE = Value(char="5", name="five", value=5)
        SIX = Value(char="6", name="six", value=6)
        SEVEN = Value(char="7", name="seven", value=7)
        EIGHT = Value(char="8", name="eight", value=8)
        NINE = Value(char="9", name="nine", value=9)
        TEN = Value(char="T", name="ten", value=10)
        JACK = Value(char="J", name="jack", value=11)
        QUEEN = Value(char="Q", name="queen", value=12)
        KING = Value(char="K", name="king", value=13)

        @classmethod
        def all(cls) -> List[Value]:
            """get all suits"""
            return sorted(
                [
                    cls.__dict__[x]
                    for x in dir(cls)
                    if not x.startswith("_") and isinstance(cls.__dict__[x], Value)
                ],
                key=lambda x: x.value,
            )

    def __init__(self, value: Value = Values.ACE, suit: Suit = Suits.SPADES) -> None:
        """card constructor"""
        self.value = value
        self.suit = suit

    @property
    def color(self) -> int:
        """returns the color of the card"""
        return self.suit.color

    @property
    def full_name(self) -> str:
        """returns the full name for this card"""
        return "{} of {}".format(self.value.name, self.suit.name)

    @property
    def is_black(self) -> bool:
        """is_black property"""
        return self.color == Card.BLACK

    @property
    def unicode(self) -> str:
        """get the fun little unicode card for this card"""
        # we need to skip the 'knight' card if we're a queen or king
        hack = int(self.value.value >= 12)
        return chr(self.suit.unicode + self.value.value + hack)

    @property
    def is_red(self) -> bool:
        """is_red property"""
        return self.color == Card.RED

    def __str__(self) -> str:
        """string representation of this card"""
        return "{}{}".format(self.value.char, self.suit.char)

    def __repr__(self) -> str:
        """representation of this card"""
        return "<Card:{}>".format(str(self))

    def __lt__(self, other: "Card") -> bool:
        """less than dunder method"""
        return self.value.value < other.value.value

    def __eq__(self, other: object) -> bool:
        """equal to dunder method"""
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value


class Deck:
    """playing card deck model"""

    def __init__(self, cards: List[Card] = None, shuffle: bool = True) -> None:
        """deck constructor"""
        if cards:
            self.cards = cards
        else:
            # lets start with a default deck of 52
            self.cards = []
            for suit in Card.Suits.all():
                for value in Card.Values.all():
                    self.cards.append(Card(value=value, suit=suit))
            self.cards.reverse()
        self.shuffles = 0
        self.draws = 0
        if shuffle:
            self.shuffle()

    def __contains__(self, item: object) -> bool:
        """dunder contains method"""
        if not isinstance(item, Card):
            return False
        return item in self.cards

    def __str__(self) -> str:
        """string representation of a deck"""
        return "<Deck[{}]>".format(self.cards_left)

    def __repr__(self) -> str:
        """term representation of a deck"""
        return str(self)

    @property
    def top(self) -> Card:
        """the top card of the deck"""
        return self.cards[-1]

    @property
    def bottom(self) -> Card:
        """the bottom card of the deck"""
        return self.cards[0]

    @property
    def cards_left(self) -> int:
        """number of cards left in the deck"""
        return len(self.cards)

    def draw(self, times: int = 1) -> Union[Card, List[Card]]:
        """draws the given number of cards from the deck"""
        if times == 1:
            self.draws += 1
            return self.cards.pop()
        cards = []
        for _ in range(times):
            self.draws += 1
            cards.append(self.cards.pop())
        return cards

    def shuffle(self, times: int = 1) -> None:
        """shuffle the deck"""
        for _ in range(times):
            self.shuffles += 1
            random.shuffle(self.cards)


class EuchreDeck(Deck):
    """deck specifically for euchre"""

    def __init__(self, **kwargs: Any) -> None:
        """euchre deck constructor"""
        cards: List[Card] = []

        # euchre uses 9, 10, J, Q, K, A of all suits
        values = [x for x in Card.Values.all() if x.value >= 9 or x.value == 1]
        for suit in Card.Suits.all():
            for value in values:
                cards.append(Card(value=value, suit=suit))
        cards.reverse()
        super().__init__(cards=cards)
