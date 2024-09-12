import sys
import os

# Adiciona o diretório 'DC-UFSCar-ES2-202401-Grupo3' ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gamble.models as g

if __name__ == "__main__":
    cards = g.BaccaratHand()
    cards.cards = ["Ja, 9a"]
    game = g.BaccaratGame()
    print(game.play_game())