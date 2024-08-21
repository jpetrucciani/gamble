from dataclasses import dataclass, field
from collections import Counter
from gamble.errors import InvalidCard
from typing import List
import random

# (Suit, Value, Card, Hand, Deck, BlackJackDeck, MultiDeck etc... já definidos anteriormente)
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

class BlackJackCard:
    """
    Cartas do Blackjack, adaptado de Card
    """

    BLACK = 0
    RED = 1

    class Suits:
        SPADES = Suit(name="spades", char="S", symbol="♠", value=0, color=0, unicode=127136)
        CLUBS = Suit(name="clubs", char="C", symbol="♣", value=1, color=0, unicode=127184)
        DIAMONDS = Suit(name="diamonds", char="D", symbol="♦", value=2, color=1, unicode=127168)
        HEARTS = Suit(name="hearts", char="H", symbol="♥", value=3, color=1, unicode=127152)

        @classmethod
        def all(cls) -> list[Suit]:
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
            return {x.char: x for x in cls.all()}

    class Values:
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
        JACK = Value(char="J", name="jack", value=10)
        QUEEN = Value(char="Q", name="queen", value=10)
        KING = Value(char="K", name="king", value=10)

        @classmethod
        def all(cls) -> list[Value]:
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
            return {x.char: x for x in cls.all()}

    def __init__(self, value: Value = Values.ACE, suit: Suit = Suits.SPADES) -> None:
        self.value = value
        self.suit = suit

    @classmethod
    def get(cls, text: str) -> "BlackJackCard":
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
        return self.suit.color

    @property
    def full_name(self) -> str:
        return f"{self.value.name} of {self.suit.name}"

    @property
    def is_black(self) -> bool:
        return self.color == BlackJackCard.BLACK

    @property
    def is_red(self) -> bool:
        return self.color == BlackJackCard.RED

    @property
    def unicode(self) -> str:
        # we need to skip the 'knight' card if we're a queen or king
        hack = int(self.value.value >= 12)
        return chr(self.suit.unicode + self.value.value + hack)

    def __str__(self) -> str:
        return f"{self.value.char}{self.suit.symbol}"

    def __repr__(self) -> str:
        return f"<BlackJackCard:{self}>"

    def __lt__(self, other: "BlackJackCard") -> bool:
        return self.value.value < other.value.value

    def __gt__(self, other: "BlackJackCard") -> bool:
        return self.value.value > other.value.value

    def __le__(self, other: "BlackJackCard") -> bool:
        return self < other or self == other

    def __ge__(self, other: "BlackJackCard") -> bool:
        return self > other or self == other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BlackJackCard):
            return False
        return self.suit == other.suit and self.value == other.value

    def shuffle(self, times: int = 1) -> None:
        """
        shuffle the deck

        Args:
            times: the number of times to shuffle the deck
        """
        for _ in range(times):
            self.shuffles += 1
            random.shuffle(self.cards)

class BlackJackHand:
    """
    Mão de BlackJack, adaptado da classe Hand
    """
    def __init__(self, cards: list[BlackJackCard]) -> None:
        self._cards = cards
        self.cards = sorted(self._cards)
        self.size = len(self.cards)
        self.value_counts = Counter([x.value.value for x in self.cards])
        self.suit_counts = Counter([x.suit.value for x in self.cards])

    def __lt__(self, other: "BlackJackHand") -> bool:
        """
        less than dunder method

        Args:
            other: another hand to compare against

        Returns:
            true if this hand is less than the other
        """
        return self.rank.value < other.rank.value

    def __gt__(self, other: "BlackJackHand") -> bool:
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

    @classmethod
    def get(cls, text: str) -> "BlackJackHand":
        """
        get a hand by text representations

        Args:
            text: a text representation of a hand

        Returns:
            a hand, if the string was valid
        """
        card_strings = text.replace(" ", "").upper().split(",")
        cards = [BlackJackCard.get(x) for x in card_strings]
        return cls(cards=cards)

class BlackJackDeck:
    def __init__(
        self, cards: list[BlackJackCard] | None = None, shuffle: bool = True, default_draw_count: int = 1,
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
        if not isinstance(item, BlackJackCard):
            return False
        return item in self.cards

    def __str__(self) -> str:
        return f"<BlackJackDeck[{self.cards_left}]>"

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, index: int) -> BlackJackCard:
        return self.cards[index]

    def clear(self) -> None:
        self.cards[:] = []

    def default_deck(self, cards: list[BlackJackCard]) -> None:
        for suit in BlackJackCard.Suits.all():
            for value in BlackJackCard.Values.all():
                cards.append(BlackJackCard(value=value, suit=suit))

    @property
    def top(self) -> BlackJackCard:
        return self.cards[-1]

    @property
    def bottom(self) -> BlackJackCard:
        return self.cards[0]

    @property
    def cards_left(self) -> int:
        return len(self.cards)

    def draw(self, times: int = -1) -> BlackJackCard | list[BlackJackCard]:
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

    def draw_hand(self, size: int = 5) -> BlackJackHand:
        cards = self.draw(times=size)
        return BlackJackHand(cards=cards if isinstance(cards, list) else [cards])

    def shuffle(self, times: int = 1) -> None:
        for _ in range(times):
            self.shuffles += 1
            random.shuffle(self.cards)
@dataclass
class BlackJackPlayer:
    name: str
    bet: int
    hand: BlackJackHand = field(default_factory=lambda: BlackJackHand([]))
    score: int = 0
    busted: bool = False
    result: str = ""
    sum: int = 0
    total: int = 0
    
    def draw(self, deck: BlackJackDeck, num_cards: int = 1) -> None:
        cards = deck.draw(times=num_cards)
        if isinstance(cards, list):
            self.hand.cards.extend(cards)
        else:
            self.hand.cards.append(cards)

    def reset_hand(self) -> None:
        self.hand = BlackJackHand([])

    def show_hand(self, dealer = False) -> None:
        if not dealer:
            print(f"{self.name}'s hand: {self.hand}")
        else:
            print(f"Dealer's hand: {self.hand.cards[0]}")

    def take_action(self, valid_actions: List[str]) -> str:
        action = input(f"{self.name}, choose your action {valid_actions}: ").strip().lower()
        while action not in valid_actions:
            action = input(f"Invalid action. Choose from {valid_actions}: ").strip().lower()
        return action

class Dealer(BlackJackPlayer):
    def should_hit(self) -> bool:
        # Regra básica para blackjack: dealer bate até 17
        return sum(card.value.value for card in self.hand.cards) < 17

class BlackJackGame:
    def __init__(self, players: List[BlackJackPlayer], deck: BlackJackDeck = BlackJackDeck()) -> None:
        self.dealer = Dealer("Dealer", 0)
        self.players = players
        self.deck = deck
        self.round_over = False

    def start_game(self) -> None:
        print("Starting a Blackjack game...")
        self.deal_initial_hands()
        self.play_round()

    def end_round(self) -> None:
        self.round_over = True

    def reset_game(self) -> None:
        for player in self.players:
            player.reset_hand()
        self.deck.shuffle()

    def deal_initial_hands(self) -> None:
        for player in self.players:
            player.draw(self.deck, num_cards=2)
            player.show_hand()
        self.dealer.draw(self.deck, num_cards=2)
        self.dealer.show_hand(dealer=True)

    def play_round(self) -> None:
        for player in self.players:
            while True:
                action = player.take_action(valid_actions=["hit", "stand"])
                if action == "hit":
                    player.draw(self.deck, num_cards=1)
                    player.show_hand()
                    if self.check_bust(player):
                        player.busted = True
                        print(f"{player.name} busted!")
                        break
                elif action == "stand":
                    break

        if self.check_bust(self.dealer):
            self.dealer = True

        for player in self.players:
            player.sum = self.get_sum_cards(player)
            if player.sum > 21:
                player.busted = True

            if player.sum == 21:
                player.result = "Win"
                player.total = player.bet + (player.bet * 1.5)
                continue

            if player.busted:
                player.result = "Lost"
                player.total = -player.bet
            elif self.dealer.busted or player.sum > self.dealer.sum:
                player.result = "Win"
                player.total = player.bet * 2
            elif player.sum < self.dealer.sum:
                player.result = "Lost"
                player.total = -player.bet
            else:
                player.result = "Push"
                player.total = 0

        print("=====Round Results=====")
        self.dealer.show_hand(dealer = False)
        for player in self.players:
            print(f"{player.name}: {player.result}, sum: {player.sum}, score: {player.total}")
        

    def get_sum_cards(self, player: BlackJackPlayer) -> int:
        return sum(card.value.value for card in player.hand.cards)
    
    def check_bust(self, player: BlackJackPlayer) -> bool:
        return sum(card.value.value for card in player.hand.cards) > 21