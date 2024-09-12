import pytest
import random
from gamble.models.BlackJack import BlackJackCard, BlackJackGame, BlackJackDeck, BlackJackHand, BlackJackPlayer

def test_init_player():
    nomes = ["Fulano", "Ciclano", "Beltrano", "Roberto"]
    apostas = [10, 20, 30, 40]

    for i in range(len(nomes)):
        player = BlackJackPlayer(nomes[i], apostas[i])
        assert player.name == nomes[i]
        assert player.bet == apostas[i]

def test_init_game():
    player = BlackJackPlayer("Fulano", 10)
    game = BlackJackGame([player])

    assert game.dealer.busted == False
    assert game.players[0].busted == False

    game.deal_initial_hands()

    assert len(game.dealer.hand) == 2
    assert len(game.players[0].hand) == 2

    game.players[0].draw(game.deck, 1)
    assert len(game.players[0].hand) == 3

    game.players[0].draw(game.deck, 30)
    assert len(game.players[0].hand) == 33

def test_player_bets():
    player = BlackJackPlayer("Fulano", 10)
    game = BlackJackGame([player])

    game.deal_initial_hands()
    game.players[0].draw(game.deck, 1)

    game.distribute_bets(game.players[0])

    if game.players[0].result == "Win":
        if game.players.sum < 21:
            assert game.players[0].total == 20
        else:
            assert game.players[0].total == 25
    elif game.players[0].result == "Lost":
        assert game.players[0].total == -10
    else:
        assert game.players[0].total == 0