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

#Teste 4 da função place_bet (Valores Quebrados)
def test5_place_bet_4():
    player = Player(balance=0.51)
    player.place_bet(amount=0.51, bet_on='Player')
    assert player.bet_amount == 0.51
    assert player.bet_on == 'Player'
    assert player.balance == 0

#Teste 5 da função place_bet (Valores Quebrados, Aposta > Balanço)
def test6_place_bet_5():
    with pytest.raises(ValueError):
        player = Player(balance=0.99)
        player.place_bet(amount=1, bet_on='Player')
        assert player.bet_on == 'Player'
        assert player.balance == 0.99

#Teste 6 da função place_bet (Aposta < Balanço)
def test7_place_bet_6():
    player = Player(balance=5)
    player.place_bet(amount=2, bet_on='Player')
    assert player.bet_on == 'Player'
    assert player.bet_amount == 2
    assert player.balance == 3

#Teste 7 da função place_bet (Valores Quebrados, Aposta < Balanço)
def test8_place_bet_7():
    player = Player(balance=1)
    player.place_bet(amount=0.99, bet_on='Player')
    assert player.bet_on == 'Player'
    assert player.bet_amount == 0.99
    assert str(player.balance)[:4] == '0.01'

#Teste 1 da função win_bet (All win)
def test9_win_bet_1():
    player=Player(balance=10)
    player.place_bet(amount=10, bet_on='Player')
    player.win_bet(payout=5)
    assert player.bet_amount == 0
    assert player.balance == 50

#Teste 2 da função win_bet (Aposta < Balanço)
def test10_win_bet_1():
    player=Player(balance=10)
    player.place_bet(amount=5, bet_on='Player')
    player.win_bet(payout=5)
    assert player.bet_amount == 0
    assert player.balance == 30
