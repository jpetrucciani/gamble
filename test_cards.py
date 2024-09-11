"""
tests for the cards submodule of gamble
"""

import pytest
import random
from gamble.models.BlackJack import BlackJackCard, BlackJackHand, Dealer
from gamble.models.Baccarat import BaccaratCard, BaccaratDeck, BaccaratHand, BaccaratGame
from gamble import (
    Card,
    Deck,
    EuchreDeck,
    Hand,
    BlackJackDeck,
    BlackJackPlayer,
    BlackJackGame,
)
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
    assert card != "test"
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


# Testes para BlackJack

def test_blackjack_card() -> None:
    card = BlackJackCard.get("AS")  # Ace of Spades
    assert card.value.name == "ace"
    assert card.suit.name == "spades"
    assert str(card) == "A♠"

def test_blackjack_card_comparison() -> None:
    card1 = BlackJackCard(value=BlackJackCard.Values.ACE, suit=BlackJackCard.Suits.HEARTS)
    card2 = BlackJackCard(value=BlackJackCard.Values.KING, suit=BlackJackCard.Suits.CLUBS)
    
    assert card1 < card2
    assert not (card1 > card2)
    assert card1 <= card2
    assert card1 != card2    

def test_invalid_card() -> None:
    with pytest.raises(InvalidCard):
        BlackJackCard.get("ZS")  # Invalid card

def test_blackjack_hand() -> None:
    cards = [BlackJackCard.get("AS"), BlackJackCard.get("TD")]
    hand = BlackJackHand(cards)
    assert len(hand) == 2
    assert hand.cards[0].value.name == "ace"
    assert hand.cards[1].suit.name == "diamonds"

def test_blackjack_deck() -> None:
    deck = BlackJackDeck()
    assert len(deck.cards) == 52
    drawn_card = deck.draw()
    assert isinstance(drawn_card, BlackJackCard)
    assert len(deck.cards) == 51

def test_blackjack_deck_methods() -> None:
    deck = BlackJackDeck(shuffle=False)
    
    # Teste de método clear
    deck.clear()
    assert len(deck.cards) == 0
    
    # Teste de método default_deck
    deck.default_deck(deck.cards)
    assert len(deck.cards) == 52  # Deve conter 52 cartas
    
    # Teste de método shuffle
    deck.shuffle()
    assert len(deck.cards) == 52  # Cartas ainda devem ser 52 após embaralhamento
    
    # Teste de método draw
    card = deck.draw()
    assert isinstance(card, BlackJackCard)
    assert len(deck.cards) == 51  # Uma carta deve ser removida
    
    # Teste de método draw_hand
    hand = deck.draw_hand(size=5)
    assert len(hand.cards) == 5

def test_blackjack_player_draw() -> None:
    deck = BlackJackDeck()
    player = BlackJackPlayer(name="TestPlayer", bet=100)
    player.draw(deck, num_cards=2)
    assert len(player.hand.cards) == 2

def test_dealer_logic() -> None:
    dealer = Dealer("Dealer", bet=0)
    deck = BlackJackDeck()
    dealer.draw(deck, num_cards=2)
    
    # Simula o comportamento do dealer
    while dealer.should_hit():
        dealer.draw(deck)
    
    assert len(dealer.hand.cards) >= 2

def test_blackjack_card_creation():
    card = BlackJackCard(BlackJackCard.Values.ACE, BlackJackCard.Suits.HEARTS)
    assert card.value == BlackJackCard.Values.ACE
    assert card.suit == BlackJackCard.Suits.HEARTS

def test_blackjack_card_unicode():
    card = BlackJackCard(BlackJackCard.Values.KING, BlackJackCard.Suits.SPADES)
    assert card.unicode == chr(BlackJackCard.Suits.SPADES.unicode + 10)

def test_blackjack_hand_value():
    cards = [
        BlackJackCard(BlackJackCard.Values.ACE, BlackJackCard.Suits.SPADES),
        BlackJackCard(BlackJackCard.Values.TEN, BlackJackCard.Suits.DIAMONDS)
    ]
    hand = BlackJackHand(cards)
    assert hand.value_counts[1] == 1
    assert hand.value_counts[10] == 1

def test_blackjack_deck_creation():
    deck = BlackJackDeck()
    assert len(deck.cards) == 52
    assert isinstance(deck.cards[0], BlackJackCard)

def test_blackjack_deck_draw():
    deck = BlackJackDeck()
    card = deck.draw()
    assert len(deck.cards) == 51
    assert isinstance(card, BlackJackCard)

def test_blackjack_player_draw():
    player = BlackJackPlayer("Fulano", bet=100)
    deck = BlackJackDeck()
    player.draw(deck, num_cards=2)
    assert len(player.hand.cards) == 2

def test_blackjack_player_busted():
    player = BlackJackPlayer("Fulano", bet=100)
    player.hand = BlackJackHand([
        BlackJackCard(BlackJackCard.Values.TEN, BlackJackCard.Suits.SPADES),
        BlackJackCard(BlackJackCard.Values.KING, BlackJackCard.Suits.HEARTS),
        BlackJackCard(BlackJackCard.Values.TWO, BlackJackCard.Suits.DIAMONDS)
    ])
    game = BlackJackGame([player])
    assert game.check_bust(player) is True

def test_blackjack_game_initial_deal():
    players = [BlackJackPlayer("Fulano", bet=100)]
    game = BlackJackGame(players)
    game.deal_initial_hands()
    assert len(players[0].hand.cards) == 2
    assert len(game.dealer.hand.cards) == 2

def test_blackjack_game_round_results(monkeypatch) -> None:
    players = [
        BlackJackPlayer("Fulano", bet=100),
        BlackJackPlayer("Beltrano", bet=100),
        BlackJackPlayer("Cicrano", bet=100)
    ]
    game = BlackJackGame(players)

    # Simular o início do jogo e as ações dos jogadores
    monkeypatch.setattr('builtins.input', lambda _: 'stand')
    game.start_game()

    for player in players:
        assert player.result in ["Win", "Lost", "Push"]  # Verificar resultados válidos

def test_invalid_card_creation():
    with pytest.raises(InvalidCard):
        BlackJackCard.get("XH")  # Valor inválido
    with pytest.raises(InvalidCard):
        BlackJackCard.get("ASD")  # Formato inválido

def test_blackjack_game_dealer_logic() -> None:
    players = [BlackJackPlayer("Player1", bet=100)]
    deck = BlackJackDeck()
    deck.shuffle()  # Embaralhe o baralho para garantir aleatoriedade
    game = BlackJackGame(players, deck)
    game.deal_initial_hands()  # Lide as cartas iniciais
    
    dealer = game.dealer
    while dealer.should_hit():
        dealer.draw(deck)
    
    # Verificar se o dealer estourou ou não
    assert not dealer.busted


# Testes para Baccarat

@pytest.fixture
def setup_game():
    game = BaccaratGame()
    return game

def test_card_initialization():
    card = BaccaratCard('A', 'ace', 1, '♠')
    assert card.char == 'A'
    assert card.name == 'ace'
    assert card.value == 1
    assert card.suit == '♠'
    assert str(card) == 'A♠'

def test_deck_initialization(setup_game):
    deck = setup_game.deck
    assert len(deck.cards) == 6 * 52  # 6 decks * 52 cards
    assert isinstance(deck.cards[0], BaccaratCard)

def test_shuffle_deck(setup_game):
    deck = setup_game.deck
    original_deck = deck.cards.copy()
    deck.shuffle()
    # Verifica se o deck foi realmente embaralhado
    assert deck.cards != original_deck
    # Verifica se o conteúdo do deck não mudou
    assert sorted(deck.cards, key=lambda card: (card.suit, card.char)) == sorted(original_deck, key=lambda card: (card.suit, card.char))


def test_draw_card(setup_game):
    deck = setup_game.deck
    card_before_draw = len(deck.cards)
    deck.draw()
    card_after_draw = len(deck.cards)
    assert card_after_draw == card_before_draw - 1

def test_hand_initialization():
    hand = BaccaratHand()
    assert len(hand.cards) == 0

def test_add_card_to_hand():
    hand = BaccaratHand()
    card = BaccaratCard('5', 'five', 5, '♠')
    hand.add_card(card)
    assert len(hand.cards) == 1
    assert hand.cards[0] == card

def test_hand_value():
    hand = BaccaratHand()
    hand.add_card(BaccaratCard('A', 'ace', 1, '♠'))
    hand.add_card(BaccaratCard('5', 'five', 5, '♠'))
    assert hand.get_value() == 6

    hand = BaccaratHand()
    hand.add_card(BaccaratCard('K', 'king', 0, '♠'))
    hand.add_card(BaccaratCard('7', 'seven', 7, '♠'))
    assert hand.get_value() == 7

def test_baccarat_game_initial_deal(setup_game):
    game = setup_game
    game.deal_initial_hands()
    assert len(game.player_hand.cards) == 2
    assert len(game.banker_hand.cards) == 2

def test_baccarat_game_play(setup_game):
    game = setup_game
    result = game.play_game()
    assert result in ["Player wins!", "Banker wins!", "Tie!"]

def test_baccarat_game_winner(setup_game):
    game = setup_game
    game.player_hand.add_card(BaccaratCard('A', 'ace', 1, '♠'))
    game.player_hand.add_card(BaccaratCard('9', 'nine', 9, '♠'))
    game.banker_hand.add_card(BaccaratCard('T', 'ten', 0, '♠'))
    game.banker_hand.add_card(BaccaratCard('8', 'eight', 8, '♠'))
    
    # Ajustar o resultado esperado conforme a lógica do Baccarat
    assert game.declare_winner() == "Banker wins!"

def test_baccarat_game_reset(setup_game):
    game = setup_game
    game.reset_game()
    assert len(game.deck.cards) == 6 * 52  # Ensure the deck is reset to original size
    assert len(game.player_hand.cards) == 0
    assert len(game.banker_hand.cards) == 0

# def test_poker_game() -> None:
#     """test a simple simulation of a poker game"""
#     game = PokerGame(num_players=4)
#     game.deal_hands()

#     for player in game.players:
#         assert len(player.hand.cards) == 5  # Cada jogador deve receber 5 cartas

#     # Simulando uma rodada de apostas
#     game.player_action(0, PlayerActions.CALL)
#     game.player_action(1, PlayerActions.RAISE, amount=10)
#     game.player_action(2, PlayerActions.FOLD)
#     game.player_action(3, PlayerActions.CALL)

#     # Finalizando o jogo e verificando o vencedor
#     winner = game.determine_winner()
#     assert winner in game.players  # O vencedor deve estar entre os jogadores
