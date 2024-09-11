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

@dataclass
class Player:
    """
    Implementação de um jogador no bacará
    """
    balance: float
    bet_amount: float = 0
    bet_on: str = "Player"  # Can be 'Player', 'Banker', or 'Tie'

    def place_bet(self, amount: float, bet_on: str):
        if amount > self.balance:
            raise ValueError("Bet amount exceeds available balance.")
        self.bet_amount = amount
        self.bet_on = bet_on

    def win_bet(self, payout: float):
        """
        Adjust the balance when the player wins the bet.
        """
        self.balance += self.bet_amount * payout
        self.bet_amount = 0

    def lose_bet(self):
        """
        Reset the bet amount when the player loses the bet.
        """
        self.bet_amount = 0


class BaccaratGame:
    """
    Implementation of the Baccarat game.
    """

    def __init__(self, player: Player):
        self.deck = BaccaratDeck()
        self.player_hand = BaccaratHand()
        self.banker_hand = BaccaratHand()
        self.player = player  # Associando o jogador ao jogo

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

        # Verificar se há um "Natural Win"
        if player_value >= 8 or banker_value >= 8:
            return self.resolve_bets()

        # Regras de terceira carta para o jogador
        if player_value <= 5:
            self.player_hand.add_card(self.deck.draw())
            player_value = self.player_hand.get_value()

        # Regra de terceira carta para o banqueiro
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

        return self.resolve_bets()

    def resolve_bets(self) -> str:
        player_value = self.player_hand.get_value()
        banker_value = self.banker_hand.get_value()

        if player_value > banker_value:
            winner = "Player"
        elif banker_value > player_value:
            winner = "Banker"
        else:
            winner = "Tie"

        print(f"Winner: {winner}")

        # Resolver as apostas
        if self.player.bet_on == winner:
            if winner == "Player":
                payout = self.player.bet_amount * 2  # 1:1 payout
                self.player.balance -= self.player.bet_amount
                self.player.balance += payout
            elif winner == "Banker":
                payout = self.player.bet_amount * 1.95  # 0.95:1 payout (5% comissão)
                self.player.balance -= self.player.bet_amount
                self.player.balance += payout
            elif winner == "Tie":
                payout = self.player.bet_amount * 8  # 8:1 payout
                self.player.balance -= self.player.bet_amount
                self.player.balance += payout
        else:
            self.player.balance -= self.player.bet_amount  # Perde a aposta

        return f"{winner} venceu! Seu novo saldo é: {self.player.balance}"

    def reset_game(self):
        self.player_hand = BaccaratHand()
        self.banker_hand = BaccaratHand()
        self.deck.shuffle()
