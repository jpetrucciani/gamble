"""
@author jacobi petrucciani
@desc standard deck of cards submodule
"""
import random
from collections import Counter
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Union
from gamble.errors import InvalidCard


class Suit(SimpleNamespace):
    """
    @desc suit namespace class
    """


class Value(SimpleNamespace):
    """
    @desc value namespace class
    """


class Rank(SimpleNamespace):
    """
    @desc hand ranks namespace class
    """


class Card:
    """
    @desc playing card model
    """

    BLACK = 0
    RED = 1

    class Suits:
        """
        @desc card suit enum
        """

        SPADES = Suit(
            name="spades", char="S", symbol="♠", value=0, color=0, unicode=127136
        )
        CLUBS = Suit(
            name="clubs", char="C", symbol="♣", value=1, color=0, unicode=127184
        )
        DIAMONDS = Suit(
            name="diamonds", char="D", symbol="♦", value=2, color=1, unicode=127168
        )
        HEARTS = Suit(
            name="hearts", char="H", symbol="♥", value=3, color=1, unicode=127152
        )

        @classmethod
        def all(cls) -> List[Suit]:
            """
            @cc 1
            @desc get all suits in this enum
            @ret a list of the suit objects
            """
            return sorted(
                [
                    cls.__dict__[x]
                    for x in dir(cls)
                    if not x.startswith("_") and isinstance(cls.__dict__[x], Suit)
                ],
                key=lambda x: x.value,
            )

        @classmethod
        def dict(cls) -> Dict[str, Suit]:
            """
            @cc 1
            @desc dict of char -> Suit
            @ret a dictionary of all the card values
            """
            return {x.char: x for x in cls.all()}

    class Values:
        """
        @desc card value enum
        """

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
            """
            @cc 1
            @desc get all suits
            @ret a list of all the values in this enum
            """
            return sorted(
                [
                    cls.__dict__[x]
                    for x in dir(cls)
                    if not x.startswith("_") and isinstance(cls.__dict__[x], Value)
                ],
                key=lambda x: x.value,
            )

        @classmethod
        def dict(cls) -> Dict[str, Value]:
            """
            @cc 1
            @desc dict of char -> Value
            @ret a dictionary of card characters to their Value representations
            """
            return {x.char: x for x in cls.all()}

    def __init__(self, value: Value = Values.ACE, suit: Suit = Suits.SPADES) -> None:
        """
        @cc 1
        @desc card constructor
        @arg value: the value of the card to create
        @arg suit: the suit of the card to create
        """
        self.value = value
        self.suit = suit

    @classmethod
    def get(cls, text: str) -> "Card":
        """
        @cc 4
        @desc get a card by text representation
        @arg text: a string representation of a card value and suit
        @ret the created card, if the string was valid
        """
        if not len(text) == 2:
            raise InvalidCard("Too many characters for a card!")
        vals = cls.Values.dict()
        suits = cls.Suits.dict()
        value_char, suit_char = list(text.upper())
        if value_char not in vals:
            raise InvalidCard("Invalid value for card!")
        if suit_char not in suits:
            raise InvalidCard("Invalid suit for card!")
        return cls(value=vals[value_char], suit=suits[suit_char])

    @property
    def color(self) -> int:
        """
        @cc 1
        @desc returns the color of the card
        @ret the color enum int for this card
        """
        return self.suit.color

    @property
    def full_name(self) -> str:
        """
        @cc 1
        @desc returns the full name for this card
        @ret the full name of this card
        """
        return f"{self.value.name} of {self.suit.name}"

    @property
    def is_black(self) -> bool:
        """
        @cc 1
        @desc is_black property
        @ret if this card is in a black suit
        """
        return self.color == Card.BLACK

    @property
    def is_red(self) -> bool:
        """
        @cc 1
        @desc is_red property
        @ret if this card is in a red suit
        """
        return self.color == Card.RED

    @property
    def unicode(self) -> str:
        """
        @cc 1
        @desc get the fun little unicode card for this card
        @ret the nice looking unicode char for the suit of this card
        """
        # we need to skip the 'knight' card if we're a queen or king
        hack = int(self.value.value >= 12)
        return chr(self.suit.unicode + self.value.value + hack)

    def __str__(self) -> str:
        """
        @cc 1
        @desc string representation of this card
        @ret a string of this card
        """
        return f"{self.value.char}{self.suit.symbol}"

    def __repr__(self) -> str:
        """
        @cc 1
        @desc representation of this card
        @ret a repr of this card
        """
        return f"<Card:{str(self)}>"

    def __lt__(self, other: "Card") -> bool:
        """
        @cc 1
        @desc less than dunder method
        @arg other: another card to compare against
        @ret true if this card is less than other
        """
        return self.value.value < other.value.value

    def __gt__(self, other: "Card") -> bool:
        """
        @cc 1
        @desc greater than dunder method
        @arg other: another card to compare against
        @ret true if this card is greater than other
        """
        return self.value.value > other.value.value

    def __le__(self, other: "Card") -> bool:
        """
        @cc 1
        @desc less than or equal to dunder method
        @arg other: another card to compare against
        @ret true if less than or equal to other
        """
        return self < other or self == other

    def __ge__(self, other: "Card") -> bool:
        """
        @cc 1
        @desc greater than or equal to dunder method
        @arg other: another card to compare against
        @ret true if this card is greater than or equal to other
        """
        return self > other or self == other

    def __eq__(self, other: object) -> bool:
        """
        @cc 2
        @desc equal to dunder method
        @arg other: another card to compare against
        @ret true if this card is the same as other
        """
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value


class Hand:
    """
    @desc playing card hand model
    """

    class Ranks:
        """
        @desc hand ranks for poker
        """

        ROYAL_FLUSH = Rank(value=9, name="royal flush")
        STRAIGHT_FLUSH = Rank(value=8, name="straight flush")
        FOUR_OF_A_KIND = Rank(value=7, name="four of a kind")
        FULL_HOUSE = Rank(value=6, name="full house")
        FLUSH = Rank(value=5, name="flush")
        STRAIGHT = Rank(value=4, name="straight")
        THREE_OF_A_KIND = Rank(value=3, name="three of a kind")
        TWO_PAIR = Rank(value=2, name="two pair")
        PAIR = Rank(value=1, name="pair")
        HIGH_CARD = Rank(value=0, name="high card")

    def __init__(self, cards: List[Card]) -> None:
        """
        @cc 1
        @desc hand constructor
        @arg cards: a list of card objects for this hand
        """
        self._cards = cards
        self.cards = sorted(self._cards)
        self.size = len(self.cards)
        self.value_counts = Counter([x.value.value for x in self.cards])
        self.suit_counts = Counter([x.suit.value for x in self.cards])

    def __lt__(self, other: "Hand") -> bool:
        """
        @cc 1
        @desc less than dunder method
        @arg other: another hand to compare against
        @ret true if this hand is less than the other
        """
        return self.rank.value < other.rank.value

    def __gt__(self, other: "Hand") -> bool:
        """
        @cc 1
        @desc greater than dunder method
        @arg other: another hand to compare against
        @ret true if this hand is greater than the other
        """
        return self.rank.value > other.rank.value

    def __len__(self) -> int:
        """
        @cc 1
        @desc dunder len method
        @ret the number of cards in this hand
        """
        return len(self.cards)

    def __str__(self) -> str:
        """
        @cc 1
        @desc string representation of the hand
        @ret this hand as a string
        """
        return f"[{', '.join([str(x) for x in self.cards])}]"

    def __repr__(self) -> str:
        """
        @cc 1
        @desc repr of the hand
        @ret this hand as repr
        """
        return f"<Hand[{self.size}]({self.rank.name}) {str(self)}>"

    @classmethod
    def get(cls, text: str) -> "Hand":
        """
        @cc 1
        @desc get a hand by text representations
        @arg text: a text representation of a hand
        @ret a hand, if the string was valid
        """
        card_strings = text.replace(" ", "").upper().split(",")
        cards = [Card.get(x) for x in card_strings]
        return cls(cards=cards)

    @property
    def rank(self) -> Rank:
        """
        @cc 10
        @desc get the rank of this hand
        @ret a rank object representing the rank of this hand
        """
        if self.is_royal_flush:
            return Hand.Ranks.ROYAL_FLUSH
        if self.is_straight_flush:
            return Hand.Ranks.STRAIGHT_FLUSH
        if self.is_four_of_a_kind:
            return Hand.Ranks.FOUR_OF_A_KIND
        if self.is_full_house:
            return Hand.Ranks.FULL_HOUSE
        if self.is_flush:
            return Hand.Ranks.FLUSH
        if self.is_straight:
            return Hand.Ranks.STRAIGHT
        if self.is_three_of_a_kind:
            return Hand.Ranks.THREE_OF_A_KIND
        if self.is_two_pair:
            return Hand.Ranks.TWO_PAIR
        if self.is_one_pair:
            return Hand.Ranks.PAIR
        return Hand.Ranks.HIGH_CARD

    @property
    def _vals(self) -> List[int]:
        """
        @cc 1
        @desc values helper to make the following checks less verbose
        @ret a sorted list of all cards in this hand
        """
        return sorted(list(self.value_counts.values()), reverse=True)

    @property
    def is_royal_flush(self) -> bool:
        """
        @cc 1
        @desc check if the hand is a royal flush
        @ret true if royal flush
        """
        return (
            self.is_flush
            and self.is_straight
            and self.cards[0].value == Card.Values.ACE
            and self.cards[-1].value == Card.Values.KING
        )

    @property
    def is_straight_flush(self) -> bool:
        """
        @cc 1
        @desc check if the hand is a straight flush
        @ret true if straight flush
        """
        return self.is_flush and self.is_straight and not self.is_royal_flush

    @property
    def is_four_of_a_kind(self) -> bool:
        """
        @cc 1
        @desc check if the hand is four of a kind
        @ret true if four of a kind
        """
        return self._vals[0] == 4

    @property
    def is_full_house(self) -> bool:
        """
        @cc 1
        @desc check if the hand is a full house
        @ret true if full house
        """
        return self._vals[0:2] == [3, 2]

    @property
    def is_flush(self) -> bool:
        """
        @cc 1
        @desc check if the hand is a flush
        @ret true if flush
        """
        return len({x.suit.value for x in self.cards}) == 1

    @property
    def is_straight(self) -> bool:
        """
        @cc 1
        @desc check if the hand is a straight
        @ret true if straight
        """

        def check(value_set: set) -> bool:
            """
            @cc 1
            @desc check if the given set is a straight
            @arg value_set: the set to check for a straight
            @ret true if this set is a straight
            """
            value_range = max(value_set) - min(value_set)
            return (value_range == self.size - 1) and (len(value_set) == self.size)

        values = [x.value.value for x in self.cards]
        low_ace = set(values)
        high_ace = set(x if x != 1 else 14 for x in values)
        return check(low_ace) or check(high_ace)

    @property
    def is_three_of_a_kind(self) -> bool:
        """
        @cc 1
        @desc check if the hand is three of a kind
        @ret true if  is three of a kind
        """
        return self._vals[0] == 3

    @property
    def is_two_pair(self) -> bool:
        """
        @cc 1
        @desc check if the hand contains two pair
        @ret true if is two pair
        """
        return self._vals[0:2] == [2, 2]

    @property
    def is_one_pair(self) -> bool:
        """
        @cc 1
        @desc check if the hand contains one pair
        @ret true if is one pair
        """
        return self._vals[0] == 2


class Deck:
    """
    @desc playing card deck model
    """

    def __init__(
        self, cards: Optional[List[Card]] = None, shuffle: bool = True
    ) -> None:
        """
        @cc 3
        @desc deck constructor
        @arg cards: a list of cards for this deck
        @arg shuffle: if we should start with the deck shuffled
        """
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
        """
        @cc 2
        @desc dunder contains method
        @arg item: the item to check for in this deck
        @ret true if this deck contains the given object
        """
        if not isinstance(item, Card):
            return False
        return item in self.cards

    def __str__(self) -> str:
        """
        @cc 1
        @desc string representation of a deck
        @ret a string representation of this deck
        """
        return f"<Deck[{self.cards_left}]>"

    def __repr__(self) -> str:
        """
        @cc 1
        @desc term representation of a deck
        @ret a repr representation of this deck
        """
        return str(self)

    @property
    def top(self) -> Card:
        """
        @cc 1
        @desc the top card of the deck
        @ret a card off the top of the deck
        """
        return self.cards[-1]

    @property
    def bottom(self) -> Card:
        """
        @cc 1
        @desc the bottom card of the deck
        @ret a card off the bottom of the deck
        """
        return self.cards[0]

    @property
    def cards_left(self) -> int:
        """
        @cc 1
        @desc number of cards left in the deck
        @ret the number of cards left
        """
        return len(self.cards)

    def draw(self, times: int = 1) -> Union[Card, List[Card]]:
        """
        @cc 3
        @desc draws the given number of cards from the deck
        @arg times: the number of times to draw
        @ret a card or list of cards drawn
        """
        if times == 1:
            self.draws += 1
            return self.cards.pop()
        cards = []
        for _ in range(times):
            self.draws += 1
            cards.append(self.cards.pop())
        return cards

    def draw_hand(self, size: int = 5) -> Hand:
        """
        @cc 1
        @desc draw a hand from this deck
        @arg size: the size of hand to draw
        @ret a hand object of size size
        """
        cards = self.draw(times=size)
        return Hand(cards=cards if isinstance(cards, list) else [cards])

    def shuffle(self, times: int = 1) -> None:
        """
        @cc 2
        @desc shuffle the deck
        @arg times: the number of times to shuffle the deck
        """
        for _ in range(times):
            self.shuffles += 1
            random.shuffle(self.cards)


class EuchreDeck(Deck):
    """
    @desc deck specifically for euchre
    """

    def __init__(self, **_: Any) -> None:
        """
        @cc 2
        @desc euchre deck constructor
        """
        cards: List[Card] = []

        # euchre uses 9, 10, J, Q, K, A of all suits
        values = [x for x in Card.Values.all() if x.value >= 9 or x.value == 1]
        for suit in Card.Suits.all():
            for value in values:
                cards.append(Card(value=value, suit=suit))
        cards.reverse()
        super().__init__(cards=cards)
