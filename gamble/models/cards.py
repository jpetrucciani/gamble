"""
deck of cards submodule
"""

import random
from collections import Counter
from dataclasses import dataclass
from typing import Any
from dataclasses import dataclass, field
from typing import List, Any
from gamble.errors import InvalidCard


@dataclass
class Suit:
    """
    suit

    Args:
        name: the name of this suit
        char: the ascii character representation for this suit
        symbol: the unicode symbol char for this suit
        value: the value of the suit
        color: the color of the suit
        unicode: the unicode id for this suit as an int
    """

    name: str
    char: str
    symbol: str
    value: int
    color: int
    unicode: int


@dataclass
class Value:
    """
    value

    Args:
        char: the ascii character representation for this value
        name: the name of the card
        value: the value of the card as an int
    """

    char: str
    name: str
    value: int


@dataclass
class Rank:
    """
    hand ranks

    Args:
        value: the integer value of the rank
        name: the name of the rank
    """

    value: int
    name: str


class Card:
    """
    playing card model

    Args:
        value: the value of the card to create
        suit: the suit of the card to create
    """

    BLACK = 0
    RED = 1

    class Suits:
        """
        card suit enum
        """

        SPADES = Suit(name="spades", char="S", symbol="♠", value=0, color=0, unicode=127136)
        CLUBS = Suit(name="clubs", char="C", symbol="♣", value=1, color=0, unicode=127184)
        DIAMONDS = Suit(name="diamonds", char="D", symbol="♦", value=2, color=1, unicode=127168)
        HEARTS = Suit(name="hearts", char="H", symbol="♥", value=3, color=1, unicode=127152)

        @classmethod
        def all(cls) -> list[Suit]:
            """
            get all suits in this enum

            Returns:
                a list of the suit objects
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
        def dict(cls) -> dict[str, Suit]:
            """
            dict of char -> Suit

            Returns:
                a dictionary of all the card values
            """
            return {x.char: x for x in cls.all()}

    class Values:
        """
        card value enum
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
        def all(cls) -> list[Value]:
            """
            get all suits

            Returns:
                a list of all the values in this enum
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
        def dict(cls) -> dict[str, Value]:
            """
            dict of char -> Value

            Returns:
                a dictionary of card characters to their Value representations
            """
            return {x.char: x for x in cls.all()}

    def __init__(self, value: Value = Values.ACE, suit: Suit = Suits.SPADES) -> None:
        self.value = value
        self.suit = suit

    @classmethod
    def get(cls, text: str) -> "Card":
        """
        get a card by text representation

        Args:
            text: a string representation of a card value and suit

        Returns:
            the created card, if the string was valid
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
        returns the color of the card

        Returns:
            the color enum int for this card
        """
        return self.suit.color

    @property
    def full_name(self) -> str:
        """
        returns the full name for this card

        Returns:
            the full name of this card
        """
        return f"{self.value.name} of {self.suit.name}"

    @property
    def is_black(self) -> bool:
        """
        is_black property

        Returns:
            if this card is in a black suit
        """
        return self.color == Card.BLACK

    @property
    def is_red(self) -> bool:
        """
        is_red property

        Returns:
            if this card is in a red suit
        """
        return self.color == Card.RED

    @property
    def unicode(self) -> str:
        """
        get the fun little unicode card for this card

        Returns:
            the nice looking unicode char for the suit of this card
        """
        # we need to skip the 'knight' card if we're a queen or king
        hack = int(self.value.value >= 12)
        return chr(self.suit.unicode + self.value.value + hack)

    def __str__(self) -> str:
        """
        string representation of this card

        Returns:
            a string of this card
        """
        return f"{self.value.char}{self.suit.symbol}"

    def __repr__(self) -> str:
        """
        representation of this card

        Returns:
            a repr of this card
        """
        return f"<Card:{self}>"

    def __lt__(self, other: "Card") -> bool:
        """
        less than dunder method

        Args:
            other: another card to compare against

        Returns:
            true if this card is less than other
        """
        return self.value.value < other.value.value

    def __gt__(self, other: "Card") -> bool:
        """
        greater than dunder method

        Args:
            other: another card to compare against

        Returns:
            true if this card is greater than other
        """
        return self.value.value > other.value.value

    def __le__(self, other: "Card") -> bool:
        """
        less than or equal to dunder method

        Args:
            other: another card to compare against

        Returns:
            true if less than or equal to other
        """
        return self < other or self == other

    def __ge__(self, other: "Card") -> bool:
        """
        greater than or equal to dunder method

        Args:
            other: another card to compare against

        Returns:
            true if this card is greater than or equal to other
        """
        return self > other or self == other

    def __eq__(self, other: object) -> bool:
        """
        equal to dunder method

        Args:
            other: another card to compare against

        Returns:
            true if this card is the same as other
        """
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value


class Hand:
    """
    playing card hand model

    Args:
        cards: a list of card objects for this hand
    """

    class Ranks:
        """
        hand ranks for poker
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

    def __init__(self, cards: list[Card]) -> None:
        self._cards = cards
        self.cards = sorted(self._cards)
        self.size = len(self.cards)
        self.value_counts = Counter([x.value.value for x in self.cards])
        self.suit_counts = Counter([x.suit.value for x in self.cards])

    def __lt__(self, other: "Hand") -> bool:
        """
        less than dunder method

        Args:
            other: another hand to compare against

        Returns:
            true if this hand is less than the other
        """
        return self.rank.value < other.rank.value

    def __gt__(self, other: "Hand") -> bool:
        """
        greater than dunder method

        Args:
            other: another hand to compare against

        Returns:
            true if this hand is greater than the other
        """
        return self.rank.value > other.rank.value

    def __len__(self) -> int:
        """
        dunder len method

        Returns:
            the number of cards in this hand
        """
        return len(self.cards)

    def __str__(self) -> str:
        """
        string representation of the hand

        Returns:
            this hand as a string
        """
        return f"[{', '.join([str(x) for x in self.cards])}]"

    def __repr__(self) -> str:
        """
        repr of the hand

        Returns:
            this hand as repr
        """
        return f"<Hand[{self.size}]({self.rank.name}) {self}>"

    @classmethod
    def get(cls, text: str) -> "Hand":
        """
        get a hand by text representations

        Args:
            text: a text representation of a hand

        Returns:
            a hand, if the string was valid
        """
        card_strings = text.replace(" ", "").upper().split(",")
        cards = [Card.get(x) for x in card_strings]
        return cls(cards=cards)

    @property
    def rank(self) -> Rank:  # noqa: PLR0911
        """
        get the rank of this hand

        Returns:
            a rank object representing the rank of this hand
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
    def _vals(self) -> list[int]:
        """
        values helper to make the following checks less verbose

        Returns:
            a sorted list of all cards in this hand
        """
        return sorted(self.value_counts.values(), reverse=True)

    @property
    def is_royal_flush(self) -> bool:
        """
        check if the hand is a royal flush

        Returns:
            true if royal flush
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
        check if the hand is a straight flush

        Returns:
            true if straight flush
        """
        return self.is_flush and self.is_straight and not self.is_royal_flush

    @property
    def is_four_of_a_kind(self) -> bool:
        """
        check if the hand is four of a kind

        Returns:
            true if four of a kind
        """
        return self._vals[0] == 4

    @property
    def is_full_house(self) -> bool:
        """
        check if the hand is a full house

        Returns:
            true if full house
        """
        return self._vals[0:2] == [3, 2]

    @property
    def is_flush(self) -> bool:
        """
        check if the hand is a flush

        Returns:
            true if flush
        """
        return len({x.suit.value for x in self.cards}) == 1

    @property
    def is_straight(self) -> bool:
        """
        check if the hand is a straight

        Returns:
            true if straight
        """

        def check(value_set: set) -> bool:
            """
            check if the given set is a straight

            Args:
                value_set: the set to check for a straight

            Returns:
                true if this set is a straight
            """
            value_range = max(value_set) - min(value_set)
            return (value_range == self.size - 1) and (len(value_set) == self.size)

        values = [x.value.value for x in self.cards]
        low_ace = set(values)
        high_ace = {x if x != 1 else 14 for x in values}
        return check(low_ace) or check(high_ace)

    @property
    def is_three_of_a_kind(self) -> bool:
        """
        check if the hand is three of a kind

        Returns:
            true if  is three of a kind
        """
        return self._vals[0] == 3

    @property
    def is_two_pair(self) -> bool:
        """
        check if the hand contains two pair

        Returns:
            true if is two pair
        """
        return self._vals[0:2] == [2, 2]

    @property
    def is_one_pair(self) -> bool:
        """
        check if the hand contains one pair

        Returns:
            true if is one pair
        """
        return self._vals[0] == 2


class Deck:
    """
    playing card deck model

    Args:
        cards: a list of cards for this deck
        shuffle: if we should start with the deck shuffled
    """

    def __init__(
        self, cards: list[Card] | None = None, shuffle: bool = True, default_draw_count: int = 1
    ) -> None:
        if cards:
            self.cards = cards
        else:
            # lets start with a default deck of 52
            self.cards = []
            self.default_deck(self.cards)
            self.cards.reverse()
        self.shuffles = 0
        self.draws = 0
        self.default_draw_count = default_draw_count
        if shuffle:
            self.shuffle()

    def __contains__(self, item: object) -> bool:
        """
        dunder contains method

        Args:
            item: the item to check for in this deck

        Returns:
            true if this deck contains the given object
        """
        if not isinstance(item, Card):
            return False
        return item in self.cards

    def __str__(self) -> str:
        """
        string representation of a deck

        Returns:
            a string representation of this deck
        """
        return f"<Deck[{self.cards_left}]>"

    def __repr__(self) -> str:
        """
        term representation of a deck

        Returns:
            a repr representation of this deck
        """
        return str(self)

    def __getitem__(self, index: int) -> Card:
        """
        get the card at the given index in the deck

        Returns:
            the card at the given index
        """
        return self.cards[index]

    def clear(self) -> None:
        """
        clear the deck of all cards
        """
        self.cards[:] = []

    def default_deck(self, cards: list[Card]) -> None:
        """
        load the standard 52 cards into the given set of cards
        """
        for suit in Card.Suits.all():
            for value in Card.Values.all():
                cards.append(Card(value=value, suit=suit))

    @property
    def top(self) -> Card:
        """
        the top card of the deck

        Returns:
            a card off the top of the deck
        """
        return self.cards[-1]

    @property
    def bottom(self) -> Card:
        """
        the bottom card of the deck

        Returns:
            a card off the bottom of the deck
        """
        return self.cards[0]

    @property
    def cards_left(self) -> int:
        """
        number of cards left in the deck

        Returns:
            the number of cards left
        """
        return len(self.cards)

    def draw(self, times: int = -1) -> Card | list[Card]:
        """
        draws the given number of cards from the deck

        Args:
            times: the number of times to draw

        Returns:
            a card or list of cards drawn
        """
        if times == -1:
            times = self.default_draw_count
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
        draw a hand from this deck

        Args:
            size: the size of hand to draw

        Returns:
            a hand object of size size
        """
        cards = self.draw(times=size)
        return Hand(cards=cards if isinstance(cards, list) else [cards])

    def shuffle(self, times: int = 1) -> None:
        """
        shuffle the deck

        Args:
            times: the number of times to shuffle the deck
        """
        for _ in range(times):
            self.shuffles += 1
            random.shuffle(self.cards)


class EuchreDeck(Deck):
    """
    deck specifically for euchre
    """

    def __init__(self, **_: Any) -> None:
        cards: list[Card] = []

        # euchre uses 9, 10, J, Q, K, A of all suits
        values = [x for x in Card.Values.all() if x.value >= 9 or x.value == 1]
        for suit in Card.Suits.all():
            for value in values:
                cards.append(Card(value=value, suit=suit))
        cards.reverse()
        super().__init__(cards=cards)


class MultiDeck(Deck):
    """
    deck consisting of multiple standard decks

    Args:
        num_decks: the number of standard decks to combine into one deck
    """

    def __init__(self, num_decks: int = 2) -> None:
        cards: list[Card] = []
        for _ in range(num_decks):
            self.default_deck(cards)
        super().__init__(cards=cards)


class BlackJackDeck(MultiDeck):
    """
    a standard blackjack shoe

    Args:
        num_decks: the number of standard decks to combine into this blackjack shoe
    """

    def __init__(self, num_decks: int = 8) -> None:
        super().__init__(num_decks=num_decks)

# (Suit, Value, Card, Hand, Deck, BlackJackDeck, MultiDeck etc... já definidos anteriormente)

@dataclass
class Player:
    name: str
    hand: Hand = field(default_factory=lambda: Hand([]))
    score: int = 0

    def draw(self, deck: Deck, num_cards: int = 1) -> None:
        cards = deck.draw(times=num_cards)
        if isinstance(cards, list):
            self.hand.cards.extend(cards)
        else:
            self.hand.cards.append(cards)

    def reset_hand(self) -> None:
        self.hand = Hand([])

    def show_hand(self) -> None:
        print(f"{self.name}'s hand: {self.hand}")

    def take_action(self, valid_actions: List[str]) -> str:
        action = input(f"{self.name}, choose your action {valid_actions}: ").strip().lower()
        while action not in valid_actions:
            action = input(f"Invalid action. Choose from {valid_actions}: ").strip().lower()
        return action

class Dealer(Player):
    def should_hit(self) -> bool:
        # Regra básica para blackjack: dealer bate até 17
        return sum(card.value.value for card in self.hand.cards) < 17

class Game:
    def __init__(self, players: List[Player], deck: Deck) -> None:
        self.players = players
        self.deck = deck
        self.round_over = False

    def start(self) -> None:
        raise NotImplementedError

    def end_round(self) -> None:
        self.round_over = True

    def reset_game(self) -> None:
        for player in self.players:
            player.reset_hand()
        self.deck.shuffle()

class PokerGame(Game):
    def start(self) -> None:
        print("Starting a Poker game...")
        self.deal_hands()
        self.play_round()

    def deal_hands(self) -> None:
        for player in self.players:
            player.draw(self.deck, num_cards=5)
            player.show_hand()

    def play_round(self) -> None:
        # Exemplo básico de interação
        for player in self.players:
            action = player.take_action(valid_actions=["fold", "check", "raise"])
            if action == "fold":
                print(f"{player.name} folded.")
            elif action == "check":
                print(f"{player.name} checks.")
            elif action == "raise":
                print(f"{player.name} raises.")
        # Decidir vencedores e pontuar aqui

class BlackJackGame(Game):
    def start(self) -> None:
        print("Starting a Blackjack game...")
        self.deal_initial_hands()
        self.play_round()

    def deal_initial_hands(self) -> None:
        for player in self.players:
            player.draw(self.deck, num_cards=2)
            player.show_hand()

    def play_round(self) -> None:
        for player in self.players:
            while True:
                action = player.take_action(valid_actions=["hit", "stand"])
                if action == "hit":
                    player.draw(self.deck, num_cards=1)
                    player.show_hand()
                    if self.check_bust(player):
                        print(f"{player.name} busted!")
                        break
                elif action == "stand":
                    break
        # Decidir vencedores e pontuar aqui

    def check_bust(self, player: Player) -> bool:
        return sum(card.value.value for card in player.hand.cards) > 21