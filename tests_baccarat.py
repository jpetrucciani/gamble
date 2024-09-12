import pytest
import random
from gamble.models.Baccarat import BaccaratCard, BaccaratDeck, BaccaratHand, BaccaratGame, Player
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

#Teste inicialização classe Player
def test1_init_player():
    player = Player(balance=0)
    assert isinstance(player, Player)
    assert player.balance == 0

#Teste 1 da função place_bet (All in)
def test2_place_bet_1():
    player = Player(balance=5)
    player.place_bet(amount=5, bet_on='Player')
    assert player.bet_amount == 5
    assert player.bet_on == 'Player'
    assert player.balance == 5

    game = BaccaratGame(player)
    result = game.play_game()

    if "Player venceu" in result:
        assert player.balance == 10
    elif "Banker vence" in result:
        assert player.balance == 0
    else:
        assert player.balance == 0

#Teste 2 da função place_bet (Aposta > Balanço)
def test3_place_bet_2():
    with pytest.raises(ValueError):
        player = Player(balance=5)
        player.place_bet(amount=6, bet_on='Player')
        assert player.bet_on == 'Player'
        assert player.balance == 5

#Teste 3 da função place_bet (Aposta e Balanço = 0)
def test4_place_bet_3():
    player = Player(balance=0)
    player.place_bet(amount=0, bet_on='Player')
    assert player.bet_amount == 0
    assert player.bet_on == 'Player'
    assert player.balance == 0

#Teste 4 da função place_bet (apostar no banker)
def test5_place_bet_4():
    player = Player(balance=100)
    player.place_bet(amount=10, bet_on='Banker')
    assert player.bet_amount == 10
    assert player.bet_on == 'Banker'
    assert player.balance == 100

    game = BaccaratGame(player)
    result = game.play_game()

    if "Player venceu" in result:
        assert player.balance == 90
    elif "Banker venceu" in result:
        assert player.balance == 109.5
    else:
        assert player.balance == 90

#Teste 5 da função place_bet (Valores Quebrados, Aposta > Balanço)
def test6_place_bet_5():
    with pytest.raises(ValueError):
        player = Player(balance=0.99)
        player.place_bet(amount=1, bet_on='Player')
        assert player.bet_on == 'Player'
        assert player.balance == 0.99

#Teste 6 da função place_bet (Aposta no empate)
def test7_place_bet_6():
    player = Player(balance=100)
    player.place_bet(amount=10, bet_on='Tie')
    assert player.bet_on == 'Tie'
    assert player.bet_amount == 10
    assert player.balance == 100

    game = BaccaratGame(player)
    result = game.play_game()

    if "Player venceu" in result:
        assert player.balance == 90
    elif "Banker venceu" in result:
        assert player.balance == 90
    else:
        assert player.balance == 170

#Teste 7 da função place_bet (Valores Quebrados, Aposta < Balanço)
def test8_place_bet_7():
    player = Player(balance=1)
    player.place_bet(amount=0.99, bet_on='Player')
    assert player.bet_on == 'Player'
    assert player.bet_amount == 0.99
