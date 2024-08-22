import random
from collections import Counter
from dataclasses import dataclass, field
from typing import List

@dataclass
class BaccaratCard:
    """
    Represents a card in the game of Baccarat.
    """
    char: str
    name: str
    value: int
    suit: str

    def __str__(self) -> str:
        return f"{self.char}{self.suit}"

class BaccaratDeck:
    """
    Represents a Baccarat deck containing multiple standard decks.
    """

    def __init__(self, num_decks: int = 6):
        self.cards = self._generate_deck(num_decks)
        self.shuffle()

    def _generate_deck(self, num_decks: int) -> List[BaccaratCard]:
        suits = ['♠', '♣', '♦', '♥']
        values = [
            BaccaratCard('A', 'ace', 1, ''), BaccaratCard('2', 'two', 2, ''), BaccaratCard('3', 'three', 3, ''),
            BaccaratCard('4', 'four', 4, ''), BaccaratCard('5', 'five', 5, ''), BaccaratCard('6', 'six', 6, ''),
            BaccaratCard('7', 'seven', 7, ''), BaccaratCard('8', 'eight', 8, ''),
            BaccaratCard('9', 'nine', 9, ''), BaccaratCard('T', 'ten', 0, ''),
            BaccaratCard('J', 'jack', 0, ''), BaccaratCard('Q', 'queen', 0, ''), BaccaratCard('K', 'king', 0, '')
        ]

        deck = []
        for _ in range(num_decks):
            for suit in suits:
                for value in values:
                    deck.append(BaccaratCard(value.char, value.name, value.value, suit))
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> BaccaratCard:
        return self.cards.pop()

class BaccaratHand:
    """
    Represents a hand in the game of Baccarat.
    """

    def __init__(self):
        self.cards: List[BaccaratCard] = []

    def add_card(self, card: BaccaratCard):
        self.cards.append(card)

    def get_value(self) -> int:
        """
        Calculates the value of a Baccarat hand. Only the last digit of the sum of values is considered.
        """
        total = sum(card.value for card in self.cards)
        return total % 10

    def __str__(self) -> str:
        return f"[{', '.join(str(card) for card in self.cards)}]"

class BaccaratGame:
    """
    Implementation of the Baccarat game.
    """

    def __init__(self):
        self.deck = BaccaratDeck()
        self.player_hand = BaccaratHand()
        self.banker_hand = BaccaratHand()

    def deal_initial_hands(self):
        self.player_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.banker_hand.add_card(self.deck.draw())
        self.banker_hand.add_card(self.deck.draw())

    def play_game(self) -> str:
        self.deal_initial_hands()
        print(f"Player's hand: {self.player_hand} (value: {self.player_hand.get_value()})")
        print(f"Banker's hand: {self.banker_hand} (value: {self.banker_hand.get_value()})")

        player_value = self.player_hand.get_value()
        banker_value = self.banker_hand.get_value()

        
        if player_value >= 8 or banker_value >= 8:
            return self.declare_winner()

        if player_value <= 5:
            self.player_hand.add_card(self.deck.draw())
            player_value = self.player_hand.get_value()

        if len(self.player_hand.cards) == 3:
            third_card_value = self.player_hand.cards[2].value
        else:
            third_card_value = None

        if banker_value <= 2:
            self.banker_hand.add_card(self.deck.draw())
        elif banker_value == 3 and third_card_value != 8:
            self.banker_hand.add_card(self.deck.draw())
        elif banker_value == 4 and third_card_value in range(2, 8):
            self.banker_hand.add_card(self.deck.draw())
        elif banker_value == 5 and third_card_value in range(4, 8):
            self.banker_hand.add_card(self.deck.draw())
        elif banker_value == 6 and third_card_value in range(6, 8):
            self.banker_hand.add_card(self.deck.draw())

        print(f"Final Player's hand: {self.player_hand} (value: {self.player_hand.get_value()})")
        print(f"Final Banker's hand: {self.banker_hand} (value: {self.banker_hand.get_value()})")

        return self.declare_winner()

    def declare_winner(self) -> str:
        player_value = self.player_hand.get_value()
        banker_value = self.banker_hand.get_value()

        if player_value > banker_value:
            return "Player wins!"
        elif banker_value > player_value:
            return "Banker wins!"
        else:
            return "Tie!"

    def reset_game(self):
        self.player_hand = BaccaratHand()
        self.banker_hand = BaccaratHand()
        self.deck.shuffle()
