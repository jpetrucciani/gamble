import sys
import os

# Adiciona o diretório 'x' ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora você pode importar os módulos do diretório 'gamble'
from gamble import models as g
from typing import List

if __name__ == "__main__":
    # print(g.BlackJackPlayer())
    players: List[g.BlackJackPlayer] = [
        g.BlackJackPlayer("Fulano", 10)
        # g.BlackJackPlayer("Ciclano", 10),
        # g.BlackJackPlayer("Beltrano", 10)
    ]

    game = g.BlackJackGame(players)
    game.players[0].sum = 21
    game.start_game()
    print(game)